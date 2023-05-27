import hashlib
import uuid

from fastapi import APIRouter

from user.schemas import UserRequest,UserResponse
from database import add_user_to_db


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/",response_model=UserResponse)
async def add_user(request: UserRequest):
    user_name = request.user_name
    
    access_token = str(uuid.uuid4())
    
    user_id = hashlib.sha256((user_name + access_token).encode()).hexdigest()
    
    await add_user_to_db(user_name, user_id, access_token)
    
    answer = {
        "user_id": user_id,
        "access_token": access_token
    }
    
    return answer
    
    