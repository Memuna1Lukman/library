from fastapi import FastAPI
from . import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)