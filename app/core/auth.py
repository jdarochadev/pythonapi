from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import oauth2_scheme
from app.database.session import get_db
from app.utils.jwt import verify_token
from app.modules.users.repository import get_user_by_username
from app.modules.users.models import User

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user
