
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi.param_functions import Depends
from fastapi import HTTPException, status
from db import db_user
    
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
SECRET_KEY = '8895e99705064b5201da9be653a7ad0b424242ae9a690d3d5314841dfd9cd83d'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentails_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentails_exception
    except JWTError:
        raise credentails_exception
    
    user = db_user.get_user_by_username(db, username)
    
    if user is None:
        raise credentails_exception
    
    return user