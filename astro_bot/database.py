# Veritabanı bağlantı modülü
import psycopg2
import json
from config import DATABASE_URL


def get_connection():
    """Veritabanına bağlantı kurar ve döndürür"""
    return psycopg2.connect(DATABASE_URL)


def create_tables():
    """Veritabanında 3 tabloyu oluşturur, tablolar zaten varsa dokunmaz"""
    conn = get_connection()  # veritabanına bağlan
    cur = conn.cursor()      # SQL sorgusu çalıştırmak için cursor aç

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id               SERIAL PRIMARY KEY,         -- otomatik artan sayı
            telegram_user_id BIGINT UNIQUE NOT NULL,     -- Telegram kullanıcı ID'si, benzersiz
            first_name       VARCHAR(100),               -- kullanıcının adı
            created_at       TIMESTAMP DEFAULT NOW(),    -- kayıt oluşturulma zamanı
            updated_at       TIMESTAMP DEFAULT NOW()     -- kayıt güncellenme zamanı
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS birth_profiles (
            id               SERIAL PRIMARY KEY,         -- otomatik artan sayı
            user_id          BIGINT REFERENCES users(telegram_user_id), -- hangi kullanıcıya ait
            birth_date       DATE,                       -- doğum tarihi
            birth_time       TIME,                       -- doğum saati
            birth_place_text VARCHAR(200),               -- doğum yeri
            latitude         FLOAT,                      -- enlem
            longitude        FLOAT,                      -- boylam
            timezone         VARCHAR(100),               -- saat dilimi
            natal_chart_json JSONB,                      -- natal chart verisi
            is_complete      BOOLEAN DEFAULT FALSE       -- profil tamamlanmış mı?
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS forecast_logs (
            id            SERIAL PRIMARY KEY,            -- otomatik artan sayı
            user_id       BIGINT REFERENCES users(telegram_user_id), -- hangi kullanıcıya ait
            period_type   VARCHAR(20),                   -- dönem tipi: daily, weekly, monthly
            period_key    VARCHAR(20),                   -- dönem anahtarı: 2026-04-21 gibi
            response_text TEXT,                          -- Groq'tan gelen Türkçe yorum
            created_at    TIMESTAMP DEFAULT NOW()        -- kayıt oluşturulma zamanı
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tablolar oluşturuldu!")


# ── GÖREV 20 ── Kullanıcı kaydetme ve okuma fonksiyonları ────────────────────

def save_user(telegram_user_id: int, first_name: str):
    """
    Kullanıcı Telegram'da /start yazdığında çağrılır.
    users tablosuna kaydeder.
    Aynı kişi tekrar yazarsa sadece ismini günceller, yeni kayıt açmaz.
    """
    conn = get_connection()  # veritabanına bağlan
    cur = conn.cursor()      # SQL sorgusu çalıştırmak için cursor aç

    cur.execute("""
        INSERT INTO users (telegram_user_id, first_name)
        VALUES (%s, %s)
        ON CONFLICT (telegram_user_id) DO UPDATE
        SET first_name = EXCLUDED.first_name,
            updated_at = NOW()
    """, (telegram_user_id, first_name))
    # ON CONFLICT → aynı kullanıcı zaten varsa hata verme, güncelle

    conn.commit()   # değişiklikleri kaydet
    cur.close()     # cursor kapat
    conn.close()    # bağlantıyı kapat


def get_user(telegram_user_id: int):
    """
    Telegram kullanıcı ID'sine göre kullanıcıyı veritabanından okur.
    Kullanıcı varsa (id, telegram_user_id, first_name) döndürür, yoksa None döndürür.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, telegram_user_id, first_name
        FROM users
        WHERE telegram_user_id = %s
    """, (telegram_user_id,))

    row = cur.fetchone()  # tek satır çek
    cur.close()
    conn.close()
    return row  # kullanıcı varsa döndür, yoksa None döndür


# ── GÖREV 21 ── Doğum profili kaydetme ve okuma fonksiyonları ────────────────

def save_birth_profile(telegram_user_id: int, birth_data: dict):
    """
    Kullanıcı doğum bilgilerini girince çağrılır.
    Kişi 2'den gelen JSON'ı birth_profiles tablosuna kaydeder.
    Böylece her seferinde tekrar hesaplatmayız, DB'den çekeriz.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO birth_profiles 
        (user_id, birth_date, birth_time, latitude, longitude, natal_chart_json, is_complete)
        VALUES (%s, %s, %s, %s, %s, %s, TRUE)
        ON CONFLICT DO NOTHING
    """, (
        telegram_user_id,
        birth_data["birth_info"]["date"],       # "1995-06-15"
        birth_data["birth_info"]["time"],       # "14:30"
        birth_data["birth_info"]["latitude"],   # 41.0082
        birth_data["birth_info"]["longitude"],  # 28.9784
        json.dumps(birth_data)                  # tüm JSON'ı sakla
    ))
    # ON CONFLICT DO NOTHING → aynı kayıt varsa hiçbir şey yapma

    conn.commit()
    cur.close()
    conn.close()


def get_birth_profile(telegram_user_id: int):
    """
    Kullanıcının daha önce kaydedilmiş doğum haritasını veritabanından okur.
    Varsa natal_chart_json döndürür, yoksa None döndürür.
    Sprint 3'te Kişi 2'ye tekrar hesaplatmamak için kullanılır.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT natal_chart_json FROM birth_profiles
        WHERE user_id = %s AND is_complete = TRUE
        ORDER BY id DESC LIMIT 1
    """, (telegram_user_id,))

    row = cur.fetchone()  # tek satır çek
    cur.close()
    conn.close()
    return row[0] if row else None  # JSON varsa döndür, yoksa None döndür


# ── GÖREV 22 ── Yorum önbellekleme fonksiyonları ─────────────────────────────

def get_cached_forecast(telegram_user_id: int, period_key: str):
    """
    Kullanıcıya bugün zaten yorum yapıldı mı kontrol eder.
    Yapıldıysa o yorumu döndürür, yapılmadıysa None döndürür.
    Böylece Groq'a gereksiz istek atmayız, kota korunur.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT response_text FROM forecast_logs
        WHERE user_id = %s AND period_key = %s
        ORDER BY created_at DESC LIMIT 1
    """, (telegram_user_id, period_key))
    # ORDER BY created_at DESC → en son yapılan yorumu al
    # LIMIT 1 → sadece 1 satır döndür

    row = cur.fetchone()  # tek satır çek
    cur.close()
    conn.close()
    return row[0] if row else None  # yorum varsa döndür, yoksa None döndür


def save_forecast(telegram_user_id: int, period_type: str, period_key: str, response_text: str):
    """
    Groq'tan gelen yorumu veritabanına kaydeder.
    Bir sonraki istekte get_cached_forecast() bunu bulur ve tekrar üretmez.
    period_type: 'daily', 'weekly', 'monthly'
    period_key: '2026-04-21' gibi tarih string'i
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO forecast_logs (user_id, period_type, period_key, response_text)
        VALUES (%s, %s, %s, %s)
    """, (telegram_user_id, period_type, period_key, response_text))

    conn.commit()  # değişiklikleri kaydet
    cur.close()
    conn.close()


if __name__ == "__main__":
    # Bu dosyayı direkt çalıştırınca tabloları oluşturur.
    # Başka dosyadan import edilince çalışmaz.
    create_tables()