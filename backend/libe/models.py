from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,TIMESTAMP,text,BigInteger,DateTime,ForeignKey



class Users(Base):
    __tablename__ = "libraryUsers"

    id = Column(Integer,primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    resources = relationship("Resource",back_populates="owner",cascade="all, delete-orphan")



class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)  # e.g., "MATH101"
    name = Column(String, nullable=False)                          # e.g., "Calculus I"
    department = Column(String, nullable=False, index=True)


    resources = relationship("Resource", back_populates="course")



class Resource(Base):
    __tablename__ = "resources"

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
    owner_id = Column(Integer, ForeignKey("libraryUsers.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="resources")
    course = relationship("Course", back_populates="resources")

    