from pydantic import BaseModel

class QuestionRequest(BaseModel):
    questions_num: int
    
class Question(BaseModel):
    id: int
    question: str
    answer:str
    created_at:str