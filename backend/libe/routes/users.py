from fastapi import APIRouter,status,HTTPException,Depends
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.NewUser,db:Session = Depends(get_db)):
    new_data = user.model_dump()
    new_data["password"] = utils.hash_password(user.password)
    new_user = models.User(**new_data)
    try:
       db.add(new_user)
       db.commit()
       db.refresh(new_user)
       return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="Registration failed. Email or Username is already taken."
        )
