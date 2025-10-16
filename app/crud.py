from sqlalchemy.orm import Session
from app import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    """Mengambil user berdasarkan email."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password: str, name: str = None):
    """Membuat user baru dengan password yang di-hash."""
    hashed_password = pwd_context.hash(password)
    user = models.User(email=email, hashed_password=hashed_password, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password: str, hashed_password: str):
    """Memverifikasi kecocokan password."""
    return pwd_context.verify(plain_password, hashed_password)

def update_user_profile(db: Session, user: models.User, name: str = None, email: str = None):
    """Memperbarui profil user (nama atau email)."""
    updated = False

    if name is not None and name != user.name:
        user.name = name
        updated = True

    if email is not None and email != user.email:
        user.email = email
        updated = True

    if not updated:
        return user

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_items(db: Session):
    """Mengambil semua item."""
    return db.query(models.Item).all()


def get_item_by_id(db: Session, item_id: int):
    """Mengambil satu item berdasarkan ID."""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def create_item(db: Session, name: str, price: int):
    """Membuat item baru."""
    item = models.Item(name=name, price=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item_id: int, name: str = None, price: int = None):
    """Memperbarui data item berdasarkan ID."""
    item = get_item_by_id(db, item_id)
    if not item:
        return None
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    """Menghapus item berdasarkan ID."""
    item = get_item_by_id(db, item_id)
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item
