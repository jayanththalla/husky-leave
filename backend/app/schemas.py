from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Literal["employee", "employer"]

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str = Field(alias="_id")
    employee_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True

# Leave Request Schemas
class LeaveRequestCreate(BaseModel):
    leave_type: str  # "casual", "sick", "annual"
    start_date: str  # ISO format
    end_date: str    # ISO format
    reason: str
    number_of_days: int

class LeaveRequestUpdate(BaseModel):
    status: Literal["approved", "rejected"]
    remarks: Optional[str] = None

class LeaveRequestResponse(BaseModel):
    id: str = Field(alias="_id")
    employee_id: str
    employee_name: str
    leave_type: str
    start_date: str
    end_date: str
    number_of_days: int
    reason: str
    status: str
    remarks: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

# Auth Response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str
