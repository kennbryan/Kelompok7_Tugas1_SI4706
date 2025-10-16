import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from app.db import SessionLocal, engine, Base
from app import models, crud

Base.metadata.create_all(bind=engine)

def seed_database():
    """Seed data awal ke database jika belum ada."""
    db = SessionLocal()
    try:
        print("Menjalankan proses seeding database...")

        user_email = "user1@example.com"
        if not crud.get_user_by_email(db, user_email):
            crud.create_user(db, user_email, "pass123", name="Demo User")
            print(f"✅ User '{user_email}' berhasil dibuat.")
        else:
            print(f"ℹ️ User '{user_email}' sudah ada, dilewati.")

        existing_items = db.query(models.Item).count()
        if existing_items == 0:
            items = [
                ("Sepatu Olahraga", 250_000),
                ("Kaos Polos", 75_000),
                ("Topi", 50_000),
            ]
            for name, price in items:
                crud.create_item(db, name, price)
            print("✅ Data item berhasil ditambahkan.")
        else:
            print(f"ℹ️ Sudah ada {existing_items} item di database, dilewati.")
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"❌ Terjadi kesalahan saat seeding: {e}")
    finally:
        db.close()
        print("✅ Proses seeding selesai.")

if __name__ == "__main__":
    seed_database()