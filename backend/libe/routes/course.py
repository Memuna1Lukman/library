from fastapi import Depends,HTTPException,status,APIRouter
from ..database import get_db
from .. import oauth2,models,schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List 
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


@router.get("/",response_model=List[schemas.CourseResponse])
def get_course(current_user = Depends(oauth2.get_current_user),db:Session = Depends(get_db)):
    query_courses = db.query(models.Course).all()
    if len(query_courses)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No course found")
    return query_courses

@router.get("/{id}",response_model=schemas.CourseResponse)
def get_by_id(id:int,current_user = Depends(oauth2.get_current_user),db:Session = Depends(get_db)):
    query_courses = db.query(models.Course).filter(
        models.Course.id == id
    ).first()
    if query_courses is None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Course with the id {id} is not found")
    return query_courses


@router.put("/{id}",response_model=schemas.CourseResponse)
def update_course(id:int,course:schemas.NewCourse,current_user= Depends(oauth2.get_current_user),db:Session = Depends(get_db)):
    # query to see whether the id is present
    courses = db.query(models.Course).filter(
        models.Course.id == id
    )
    query_courses = courses.first()
    if query_courses is None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Course with the id {id} is not found")

    courses.update(query_courses.dict(exclude_unset = True),synchronize_session=False)
    db.commit()
    db.refresh(query_courses)
    return query_courses

    # then make sure you update each row like you like it


    
@router.delete("/{id}")
def del_course(id:int,current_user = Depends(oauth2.get_current_user),db:Session = Depends(get_db)):
    query_courses = db.query(models.Course).filter(models.Course.id == id)
    query = query_courses.first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="course not found")
    query_courses.delete(synchronize_session=False)
    db.commit()
    return {"statas" : "Delete successful"}