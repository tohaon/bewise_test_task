from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert,desc, select, and_ 

from questions.model import Question
from user.model import User
from record.model import Audio

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def add_to_db(id, question, answer, created_at):
    async with async_session_maker() as session:
        stmt = insert(Question).values(
            id=id,
            question=question,
            answer=answer,
            created_at=created_at
        )
        await session.execute(stmt)
        await session.commit()

async def get_last():
    async with async_session_maker() as session:
        stmt = select(Question).order_by(desc(Question.pk)).limit(1)
        result = await session.execute(stmt)
        record = result.scalar()
        
        last_question = {
            "id": record.id,
            "question" : record.question,
            "answer" : record.answer,
            "created_at" : record.created_at
        }
        
        return last_question
    
async def check_id(id:int) -> bool:
    async with async_session_maker() as session:
        stmt = select(Question.pk).where(Question.id==id)
        check = await session.execute(stmt)
        
        if check.scalar():
            return True
        return False
    
    
async def add_user_to_db(name:str, id:str, token:str):
    async with async_session_maker() as session:
        stmt = insert(User).values(
            user_name=name,
            user_id=id,
            access_token=token
        )
        await session.execute(stmt)
        await session.commit()
        
        
async def legit_user(user_id:str, access_token:str) -> bool:  
    async with async_session_maker() as session:
        stmt = select(User.access_token).where(User.user_id==user_id)
        check = await session.execute(stmt)
        
        await session.execute(stmt)
        await session.commit()
        
        if check.scalar() == access_token:
            return True
        return False
 
async def add_record_to_db(uuid: str, user_id:str, audio):
    async with async_session_maker() as session:
        stmt = select(Audio).where(and_(Audio.audio==audio, Audio.user_id==user_id))
        result = await session.execute(stmt)
        existing_audio = result.scalar_one_or_none()
        
        if existing_audio is not None:
            return False
        
        stmt = insert(Audio).values(
            uuid=uuid,
            user_id=user_id,
            audio=audio
        )
        await session.execute(stmt)
        await session.commit()
        
        return True
    
async def get_record(uuid:str, user_id:str):
    async with async_session_maker() as session:
        stmt = select(Audio.audio).where(and_(Audio.uuid==uuid, Audio.user_id==user_id))
        audio = await session.execute(stmt)
        
        await session.execute(stmt)
        await session.commit()
        
        return audio.scalar()
        
        