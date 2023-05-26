import requests
from fastapi import HTTPException

def get_questions_api(questions_num:int) -> list:
    URL = f"https://jservice.io/api/random?count={questions_num}"
    
    try:
        response = requests.get(URL)
    except:
        raise HTTPException(status_code=404, detail="Something went wrong")
    
    json_list = response.json()
    
    return json_list