from fastapi import FastAPI
from . import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth,users,upload,course


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(course.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)