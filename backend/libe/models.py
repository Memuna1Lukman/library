from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,TIMESTAMP,text,BigInteger,DateTime,ForeignKey



class Users(Base):
    __tablename__ = "libraryUsers"

    id = Column()
    username = Column()
    email = Column()
    password = Column()


    resources = relationship("Resource",back_populates="owner",cascade="all, delete-orphan")



class Course(Base):
    id = Column()
    code = Column()
    name = Column()
    department = Column()


    resources = relationship("Resource", back_populates="course")



class Resource(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    file_path = Column(String, nullable=False)            # Unique internal path (UUID-based)
    original_filename = Column(String, nullable=False)    # Display name for user download
    file_size_bytes = Column(BigInteger, nullable=False)  # For tracking storage quota
    mime_type = Column(String, nullable=False)            # e.g., "application/pdf"
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  #there is a lot function with the 
    # Foreign Keys
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="resources")
    course = relationship("Course", back_populates="resources")

    