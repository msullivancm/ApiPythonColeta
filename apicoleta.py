from coleta import Coleta
import numpy as np 
from fastapi import FastAPI
from fastapi import Response

app = FastAPI()

SQLALCHEMY_DATABASE_URI = 'sqlite:///banco.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

array = coleta()
dictteste = {a: b for a, b in array}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/dados")
async def dados():
    return dictteste

#Iniciar servidor: python -m uvicorn apicoleta:app --reload

