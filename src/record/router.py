import uuid
import shutil
import os

from fastapi.responses import FileResponse 
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydub import AudioSegment

from database import add_record_to_db, legit_user, get_record

router = APIRouter(
    prefix="/record",
    tags=["Record"]
)

@router.get("/")
async def download_file(id:str, user:str):
    audio = await get_record(id, user)
    with open('./record/storage/record.mp3', 'wb') as f:
        f.write(audio)
    
    return FileResponse(path='./record/storage/record.mp3', filename='Music.mp3', media_type='multipart/form-data')


@router.post("/")
async def add_record(user_id:str, access_token:str, file:UploadFile = File(..., content_type="audio/wav")):
    have_access = await legit_user(user_id, access_token)
    if not have_access:
        raise HTTPException(status_code=422, detail="Неверные данные пользователя")
        
    if file.filename[-4:] != ".wav":
        raise HTTPException(status_code=422, detail="Неверный формат файла")

    try:
        with open('./record/storage/'+ file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        raise HTTPException(status_code=422, detail="Проблемы с загрузкой файла")
    finally:
        file.file.close()
        
    audio = AudioSegment.from_mp3(f"./record/storage/{file.filename}")
    save_audio = audio.export(f"./record/storage/sample-3s.mp3", format="wav").read()
    audio_id = str(uuid.uuid4())   
    
    for file in os.listdir('./record/storage/'):
        file_path = os.path.join('./record/storage/', file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    add = await add_record_to_db(audio_id, user_id, save_audio)
    if add == False:
        raise HTTPException(status_code=422, detail="Вы уже добавили данную аудиозапись в базу данных")
    
    return f"http://localhost:9999/record?id={audio_id}&user={user_id}"

