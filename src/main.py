from fastapi import FastAPI

from questions.router import router as question_router
from user.router import router as user_router
from record.router import router as record_router

app = FastAPI(
    title="bewise_test"
)

app.include_router(question_router)
app.include_router(user_router)
app.include_router(record_router)