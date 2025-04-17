from fastapi import FastAPI,HTTPException,status,Depends
from database import user_collection,token_collection
from models import RegisterUser,LoginUser
from auth import hash_password,verify_password,validate_token
from auth import get_user_by_email,get_user_by_mobile,authenticate_user
from auth import create_access_token,create_refresh_token
from datetime import datetime,timedelta
from bson import ObjectId

import os

app = FastAPI()

@app.get('/',tags=["User Management"])
async def home():
    return {"message":"Welcome to fastapi user-management"}



@app.post("/user/register", tags=["User Management"])
async def register(user: RegisterUser):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already exists.")
    if get_user_by_mobile(user.mobile):
        raise HTTPException(status_code=400, detail="Mobile number already exists.")
    hashed_password = hash_password(user.password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password
    user_data.pop("password")
    user_data["created_at"] = datetime.utcnow()
    user_data["updated_at"] = datetime.utcnow()
    user_data["is_active"] = False
    new_user = user_collection.insert_one(user_data)
    return {
        "message": "User registered successfully",
        "id": str(new_user.inserted_id)
    }

@app.post("/user/login", tags=["User Management"])
async def login(user:LoginUser):
    # 1. Authenticate user
    user = authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 2. Create tokens
    access_token = create_access_token(data={"sub": user['email'], "id": str(user['_id'])})
    refresh_token = create_refresh_token(data={"sub": user['email'], "id": str(user['_id'])})

    # 3. Handle token storage
    now = datetime.utcnow()
    expires_at = now + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 480)))

    db_token = token_collection.find_one({"user_id": user['_id']})
    if db_token:
        token_collection.update_one(
            {"user_id": user["_id"]},
            {"$set": {
                "token": access_token,
                "created_at": now,
                "expires_at": expires_at
            }}
        )
    else:
        token_collection.insert_one({
            "user_id": user["_id"],
            "token": access_token,
            "created_at": now,
            "expires_at": expires_at
        })

    # 4. Update user status
    user_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"is_active": True, "updated_at": now}}
    )

    # 5. Return response
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "user_id": str(user['_id']),
    }

@app.get("/user/me", tags=["User Management"])
async def my_details(token: dict = Depends(validate_token)):
    """
    Get the current logged-in user's details.
    The token will be validated, and the user will be fetched based on email or mobile.
    """
    user = token  # The user returned by the validate_token function
    
    # Ensure that the user is not None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user["_id"] = str(user["_id"])  # Ensure the ObjectId is serialized as a string
    return user

@app.post("/user/logout/{user_id}", tags=["User Management"])
async def logout(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    token_collection.delete_one({"user_id": ObjectId(user_id)})

    return {"detail": "User logged out successfully"}

