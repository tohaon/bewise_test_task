from fastapi import APIRouter
from questions.schemas import QuestionRequest, Question

from database import add_to_db, get_last, check_id
from questions.api_requests import get_questions_api


router = APIRouter(
    prefix="/question",
    tags=["Question"]
)

@router.post("/", response_model=Question)
async def get_questions(request: QuestionRequest):
    question_list = get_questions_api(request.questions_num)
    
    for obj in question_list:
        existence = await check_id(obj['id'])
        
        if not existence:
            await add_to_db(obj['id'], obj['question'], obj['answer'], obj['created_at'])  
        else:
            while existence:
                new_question = get_questions_api(1)
                existence = await check_id(new_question[0]['id'])
          
            await add_to_db(new_question['id'], new_question['question'], new_question['answer'], new_question['created_at'])
        
    last_question = await get_last()
    return last_question
