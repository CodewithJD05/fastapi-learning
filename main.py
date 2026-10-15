from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from config import settings
app = FastAPI()

load_dotenv()
# ALLOWED ORIGINS(FRONT-END URL)
origins = settings.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins #ALLOWED FE
    allow_credentials=True,
    allow_methods=["*"], #GET,PUT,POST,DELETE
    allow_headers=["*"]  
)

@app.get("/")
def home():
    return{ 
        "message":"CORS ENABLE API"
    }