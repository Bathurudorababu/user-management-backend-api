from passlib.context import CryptContext
from database import user_collection
from datetime import datetime,timedelta
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(email:str) -> dict:
    return user_collection.find_one({"email":email})

def get_user_by_mobile(mobile: str) -> dict:
    return user_collection.find_one({"phone": mobile})

def authenticate_user(email: str, password: str):
    user = user_collection.find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user.get("hashed_password", "")):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    # print(type(to_encode))
    #token expire time is now 8 hours
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=480))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))  # Refresh token lasts longer
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, ExpiredSignatureError
from database import token_collection
security = HTTPBearer()

# Function to validate the token
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    db_token = token_collection.find_one({"token": token})

    # Token not found in the database
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if the token has expired (custom expiration logic, not JWT expiration)
    if db_token.get("expires_at") and db_token["expires_at"] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        sub = payload.get("sub")  # 'sub' is typically the user identifier (email or mobile)

        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Determine if the sub is an email or mobile and fetch the user accordingly
        user = None
        if "@" in sub:  # If it contains '@', it must be an email
            user = get_user_by_email(sub)  # Fetch user by email
        else:  # If it's not an email, assume it's a mobile number
            user = get_user_by_mobile(sub)  # Fetch user by mobile

        # If the user is not found, raise an error
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user  # Return the user object for further use

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        # Catch other JWT errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
