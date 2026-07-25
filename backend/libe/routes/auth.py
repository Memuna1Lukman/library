from fastapi import HTTPException,Depends,status,APIRouter
from .. import models,utils,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags= ["Logs"],
    prefix="/login"
)

@router.post("/")
def login_user(user:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    check_user = db.query(models.Users).filter(models.Users.email == user.username).first()
    if not check_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
    verify_password = utils.unhash_password(user.password,check_user.password)
    if not verify_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are an authorized user")
    
          