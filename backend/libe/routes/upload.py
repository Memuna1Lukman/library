from fastapi import Depends,status,HTTPException,APIRouter,UploadFile,File
import magic
from ..database import get_db
from .. import models,schemas



route = APIRouter(
    tags=['Upload'],
    prefix="/uploads"
)


ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "application/pdf"]

