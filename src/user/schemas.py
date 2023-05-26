from pydantic import BaseModel

class UserRequest(BaseModel):
    user_name: str
    
class UserResponse(BaseModel):
    user_id: str
    access_token: str