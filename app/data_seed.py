from app.db import SessionLocal, engine, Base
from app import models, crud

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not crud.get_user_by_email(db, "user1@example.com"):
            crud.create_user(db, "user1@example.com", "pass123", name="Demo User")
        if not db.query(models.Item).first():
            crud.create_item(db, "Sepatu Olahraga", 250000, db=db)
            crud.create_item(db, "Kaos Polos", 75000, db=db)
            crud.create_item(db, "Topi", 50000, db=db)
    finally:
        db.close()

if __name__ == '__main__':
    seed()