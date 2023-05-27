import uuid
import shutil
import os

from fastapi.responses import FileResponse 
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydub import AudioSegment
from starlette.background import BackgroundTasks

from database import add_record_to_db, legit_user, get_record

router = APIRouter(
    prefix="/record",
    tags=["Record"]
)

def remove_file(path: str) -> None:
    os.remove(path)

@router.get("/")
async def download_file(id:str, user:str,background_tasks: BackgroundTasks):
    audio = await get_record(id, user)
    path = f'./record/storage/{id}.mp3'
    with open(path, 'wb') as f:
        f.write(audio)
    
    background_tasks.add_task(remove_file, path)
    return FileResponse(path=path, filename='Music.mp3', media_type='multipart/form-data')


@router.post("/")
async def add_record(user_id:str, access_token:str, file:UploadFile = File(..., content_type="audio/wav")):
    have_access = await legit_user(user_id, access_token)
    if not have_access:
        raise HTTPException(status_code=422, detail="Invalid user data")
        
    if file.filename[-4:] != ".wav":
        raise HTTPException(status_code=422, detail="Invalid file format")

    try:
        with open('./record/storage/'+ file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        raise HTTPException(status_code=422, detail="Problems with downloading the file")
    finally:
        file.file.close()
    
    audio_id = str(uuid.uuid4())    
    audio = AudioSegment.from_mp3(f"./record/storage/{file.filename}")
    save_audio = audio.export(f"./record/storage/{audio_id}.mp3", format="wav").read()
      
    
    for file in os.listdir('./record/storage/'):
        file_path = os.path.join('./record/storage/', file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    add = await add_record_to_db(audio_id, user_id, save_audio)
    if add == False:
        raise HTTPException(status_code=422, detail="You have already added this audio recording to the database")
    
    return f"http://localhost:9999/record?id={audio_id}&user={user_id}"

