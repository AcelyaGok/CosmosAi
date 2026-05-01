# tests/test_db_connection.py
import sys
import os

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)

from astro_bot.config import DATABASE_URL
from astro_bot.database import get_connection


print("=" * 60)
print("DB BAĞLANTI TESTİ")
print("=" * 60)

# Test 1: DATABASE_URL .env'den okunuyor mu?
print("\nTEST 1: DATABASE_URL okunuyor mu?")
if DATABASE_URL:
    # Şifreyi gizleyerek göster (güvenlik için)
    safe_url = DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "geçersiz format"
    print(f"  ✅ DATABASE_URL var: ...@{safe_url}")
else:
    print(f"  ❌ DATABASE_URL boş veya bulunamadı!")
    sys.exit(1)

# Test 2: Bağlantı kurulabiliyor mu?
print("\nTEST 2: DB'ye bağlanılıyor mu?")
try:
    conn = get_connection()
    print(f"  ✅ Bağlantı başarılı")
except Exception as e:
    print(f"  ❌ Bağlantı hatası: {type(e).__name__}")
    print(f"     Detay: {e}")
    sys.exit(1)

# Test 3: Basit bir sorgu çalıştırılabiliyor mu?
print("\nTEST 3: Sorgu çalıştırılabiliyor mu?")
try:
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    print(f"  ✅ PostgreSQL sürümü: {version[:50]}...")
    cur.close()
except Exception as e:
    print(f"  ❌ Sorgu hatası: {e}")
    conn.close()
    sys.exit(1)

# Test 4: Hangi tablolar var?
print("\nTEST 4: Mevcut tablolar")
try:
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = [row[0] for row in cur.fetchall()]
    if tables:
        print(f"  Bulunan tablolar: {tables}")
        # Beklediğimiz 3 tablo var mı?
        beklenen = {"users", "birth_profiles", "forecast_logs"}
        mevcut = set(tables)
        if beklenen.issubset(mevcut):
            print(f"  ✅ Tüm gerekli tablolar mevcut")
        else:
            eksik = beklenen - mevcut
            print(f"  ⚠️ Eksik tablolar: {eksik}")
            print(f"     create_tables() çağrılmalı")
    else:
        print(f"  ⚠️ Hiç tablo yok — create_tables() çağrılmalı")
    cur.close()
except Exception as e:
    print(f"  ❌ Tablo listesi hatası: {e}")

conn.close()

print("\n" + "=" * 60)
print("TEST BİTTİ")
print("=" * 60)