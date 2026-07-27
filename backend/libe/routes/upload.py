from fastapi import Depends,status,HTTPException,APIRouter,UploadFile,File,Form
import magic
import os
import uuid
from ..database import get_db
from .. import models,schemas,oauth2
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

router = APIRouter(
    tags=['Upload'],
    prefix="/uploads"
)


ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "application/pdf"]
MAX_FILE_SIZE = 10*1024*1024
UPLOAD_DIR = "./uploaded_files"


os.makedirs(UPLOAD_DIR,exist_ok=True)

@router.post("/")
async def upload_files(
    title:str = Form(...),
    description:str = Form(...),
    file:UploadFile = File(...),
    
    course_id:int=Form(...),
    db:Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
):
    contents = bytearray()
    while chunk := await file.read(1024*1024):
        contents.extend(chunk)
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds maximum limit of 10 MB.",
           )

    courses = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not courses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} does not exist."
        )
    mime_type = magic.from_buffer(bytes(contents),mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The file type is not allowed")


    # how to give the file a unique name
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR,unique_filename)

    with open(file_path,"wb") as f:
        f.write(contents)

   
    new_resources = models.Resource(
        title = title,
        description = description,
        file_path = file_path,        
        owner_id = current_user.id,
        course_id = courses.id
    )    

    db.add(new_resources)
    db.commit()
    db.refresh(new_resources)
    return new_resources




   
   
   
@router.get("/download/{resource_id}")
async def download_resource(
    resource_id : int,
    db:Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found."
        )
    if not os.path.exists(resource.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File content missing on server."
        )
    file_ext = os.path.splitext(resource.file_path)[1]
    safe_download_name = f"{resource.title.replace(' ', '_')}{file_ext}"
    resource.download_count+=1
    db.commit()
    return FileResponse(
        path= resource.file_path,
        media_type = resource.mime_type,
        filename=safe_download_name
    )