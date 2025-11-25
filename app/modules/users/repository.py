from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate
from app.utils.hashing import hash_password

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()
