# Veritabanı bağlantı modülü
import psycopg2
from config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id               SERIAL PRIMARY KEY,
            telegram_user_id BIGINT UNIQUE NOT NULL,
            first_name       VARCHAR(100),
            created_at       TIMESTAMP DEFAULT NOW(),
            updated_at       TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS birth_profiles (
            id               SERIAL PRIMARY KEY,
            user_id          BIGINT REFERENCES users(telegram_user_id),
            birth_date       DATE,
            birth_time       TIME,
            birth_place_text VARCHAR(200),
            latitude         FLOAT,
            longitude        FLOAT,
            timezone         VARCHAR(100),
            natal_chart_json JSONB,
            is_complete      BOOLEAN DEFAULT FALSE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS forecast_logs (
            id            SERIAL PRIMARY KEY,
            user_id       BIGINT REFERENCES users(telegram_user_id),
            period_type   VARCHAR(20),
            period_key    VARCHAR(20),
            response_text TEXT,
            created_at    TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tablolar oluşturuldu!")

if __name__ == "__main__":
    create_tables() 