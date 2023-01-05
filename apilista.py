from fastapi import FastAPI
import pandas as pd
import json
from classes.coleta import Coleta

def parse_plan(df):
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed

base = r'H:\TI\Sistemas\PowerBI Ferroport\AutomacaoKPIsPowerBI'
dir = 'planner'
tipo = 'xlsx'
arqnames = ['TI_Infraestrutura.xlsx','TI_Sistemas.xlsx']

df = Coleta(base, dir, tipo, arqnames)

app = FastAPI()
lista_de_dfs = []
for i in arqnames:
    #print(f"{base}\{dir}\{i}")
    lista_de_dfs.append(parse_plan(pd.read_excel(f"{base}\{dir}\{i}")))
#print(lista_de_dfs)

@app.get("/"+dir)
def load_dados():
    return lista_de_dfs
    
#load server: python -m uvicorn apilista:app --reload

#No power bi tem que criar uma fonte de dados com o seguinte: 
'''
let
    Source = Json.Document(File.Contents('http://127.0.0.1:8000/planner')),
in
    Source
'''