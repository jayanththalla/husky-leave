from fastapi import APIRouter, HTTPException, Depends, Header, Query
from bson import ObjectId
from datetime import datetime
from app.schemas import LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestResponse, MessageResponse
from app.auth import verify_token
from app.database import get_database
from typing import List, Optional

router = APIRouter(prefix="/api/leaves", tags=["leaves"])

def get_current_user_from_header(authorization: Optional[str] = Header(None), db=Depends(get_database)):
    """Extract and verify token from Authorization header"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = authorization[7:]  # Remove "Bearer " prefix
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@router.post("/request", response_model=LeaveRequestResponse)
async def create_leave_request(
    request: LeaveRequestCreate,
    current_user = Depends(get_current_user_from_header),
    db=Depends(get_database)
):
    """Create a new leave request (Employee only)"""
    if current_user["role"] != "employee":
        raise HTTPException(status_code=403, detail="Only employees can create leave requests")
    
    leave_request = {
        "employee_id": current_user.get("employee_id"),
        "employee_name": current_user["full_name"],
        "user_id": str(current_user["_id"]),
        "leave_type": request.leave_type,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "number_of_days": request.number_of_days,
        "reason": request.reason,
        "status": "pending",
        "remarks": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    
    result = db.leave_requests.insert_one(leave_request)
    new_request = db.leave_requests.find_one({"_id": result.inserted_id})
    
    return {
        "_id": str(new_request["_id"]),
        "employee_id": new_request["employee_id"],
        "employee_name": new_request["employee_name"],
        "leave_type": new_request["leave_type"],
        "start_date": new_request["start_date"],
        "end_date": new_request["end_date"],
        "number_of_days": new_request["number_of_days"],
        "reason": new_request["reason"],
        "status": new_request["status"],
        "remarks": new_request.get("remarks"),
        "created_at": new_request["created_at"],
        "updated_at": new_request["updated_at"],
    }

@router.get("/my-requests", response_model=List[LeaveRequestResponse])
async def get_my_leave_requests(
    current_user = Depends(get_current_user_from_header),
    db=Depends(get_database)
):
    """Get current user's leave requests"""
    if current_user["role"] == "employee":
        requests = list(db.leave_requests.find({"user_id": str(current_user["_id"])}).sort("created_at", -1))
    else:
        requests = list(db.leave_requests.find().sort("created_at", -1))
    
    return [
        {
            "_id": str(req["_id"]),
            "employee_id": req["employee_id"],
            "employee_name": req["employee_name"],
            "leave_type": req["leave_type"],
            "start_date": req["start_date"],
            "end_date": req["end_date"],
            "number_of_days": req["number_of_days"],
            "reason": req["reason"],
            "status": req["status"],
            "remarks": req.get("remarks"),
            "created_at": req["created_at"],
            "updated_at": req["updated_at"],
        }
        for req in requests
    ]

@router.get("/all", response_model=List[LeaveRequestResponse])
async def get_all_leave_requests(
    status: Optional[str] = Query(None),
    current_user = Depends(get_current_user_from_header),
    db=Depends(get_database)
):
    """Get all leave requests (Employer only)"""
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Only employers can view all requests")
    
    query = {}
    if status:
        query["status"] = status
    
    requests = list(db.leave_requests.find(query).sort("created_at", -1))
    
    return [
        {
            "_id": str(req["_id"]),
            "employee_id": req["employee_id"],
            "employee_name": req["employee_name"],
            "leave_type": req["leave_type"],
            "start_date": req["start_date"],
            "end_date": req["end_date"],
            "number_of_days": req["number_of_days"],
            "reason": req["reason"],
            "status": req["status"],
            "remarks": req.get("remarks"),
            "created_at": req["created_at"],
            "updated_at": req["updated_at"],
        }
        for req in requests
    ]

@router.patch("/{request_id}", response_model=LeaveRequestResponse)
async def update_leave_request(
    request_id: str,
    update: LeaveRequestUpdate,
    current_user = Depends(get_current_user_from_header),
    db=Depends(get_database)
):
    """Update leave request status (Employer only)"""
    if current_user["role"] != "employer":
        raise HTTPException(status_code=403, detail="Only employers can update requests")
    
    try:
        obj_id = ObjectId(request_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid request ID")
    
    updated = db.leave_requests.find_one_and_update(
        {"_id": obj_id},
        {
            "$set": {
                "status": update.status,
                "remarks": update.remarks,
                "updated_at": datetime.now(),
            }
        },
        return_document=True
    )
    
    if not updated:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    return {
        "_id": str(updated["_id"]),
        "employee_id": updated["employee_id"],
        "employee_name": updated["employee_name"],
        "leave_type": updated["leave_type"],
        "start_date": updated["start_date"],
        "end_date": updated["end_date"],
        "number_of_days": updated["number_of_days"],
        "reason": updated["reason"],
        "status": updated["status"],
        "remarks": updated.get("remarks"),
        "created_at": updated["created_at"],
        "updated_at": updated["updated_at"],
    }
