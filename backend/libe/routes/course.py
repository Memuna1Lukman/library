from fastapi import Depends,HTTPException,status,APIRouter
from ..database import get_db
from .. import oauth2,models,schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    tags=["Courses"],
    prefix="/courses"
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.CourseResponse)
def create_course(course:schemas.NewCourse,current_user= Depends(oauth2.get_current_user),db:Session = Depends(get_db)):
    # query the users table to see if the user is the current user and is authorized
    # this is redundant because the current_user will do that job and so i do not need to do this

    # query_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    # if not query_user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are an authorized user")
    
    try:
        new_course = course.model_dump()
        add_course = models.Course(**new_course)
        db.add(add_course)
        db.commit()
        db.refresh(add_course)
        return add_course
    except  IntegrityError:
        db.rollback()
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="failed course already in the system."
                )   



