
from typing import Optional
from typing_extensions import Annotated
from datetime import timedelta
from datetime import datetime
import time
from fastapi import HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
# from database.database import Settings
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

ALGORITHM = "HS256"
JWT_SECRET_KEY = "foo"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Create a CryptContext object to manage password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


#data={"user":1,"exp":3600}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        data = jwt.decode(token, JWT_SECRET_KEY,
        algorithms=ALGORITHM)
        expire = data.get("exp")
        if expire is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No access token supplied"
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired!"
            )
        return data
    
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token"
        )


# Create a get_current_user dependency (this is used for protected routes)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token=token)
