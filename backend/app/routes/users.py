from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from app.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from app.auth import hash_password, verify_password, create_access_token, verify_token
from app.database import get_database
import uuid

router = APIRouter(prefix="/api/users", tags=["users"])

def get_current_user(db=Depends(get_database)):
    """Placeholder for getting current user from token"""
    async def _get_current_user(token: str = None):
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    return _get_current_user

@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate, db=Depends(get_database)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user_dict = {
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "password_hash": hash_password(user.password),
        "created_at": datetime.now(),
    }
    
    if user.role == "employee":
        user_dict["employee_id"] = f"EMP-{str(uuid.uuid4())[:8].upper()}"
    
    result = db.users.insert_one(user_dict)
    new_user = db.users.find_one({"_id": result.inserted_id})
    
    # Create token
    access_token = create_access_token(
        data={"sub": str(new_user["_id"]), "email": new_user["email"], "role": new_user["role"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "_id": str(new_user["_id"]),
            "email": new_user["email"],
            "full_name": new_user["full_name"],
            "role": new_user["role"],
            "employee_id": new_user.get("employee_id"),
            "created_at": new_user["created_at"],
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db=Depends(get_database)):
    """Login user"""
    user = db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create token
    access_token = create_access_token(
        data={"sub": str(user["_id"]), "email": user["email"], "role": user["role"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "_id": str(user["_id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "employee_id": user.get("employee_id"),
            "created_at": user["created_at"],
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(token: str, db=Depends(get_database)):
    """Get current user profile"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "_id": str(user["_id"]),
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "employee_id": user.get("employee_id"),
        "created_at": user["created_at"],
    }

from datetime import datetime
