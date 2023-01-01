from configparser import ConfigParser
import pandas as pd
import openpyxl

def coleta():
    config = ConfigParser()
    config.read("config.ini")

    #print(config.sections())
    arq=[]
    dfa=[]
    base = config.get('arquivos','base')
    dir = config.get('planner','dir')
    tipo = config.get('planner','tipo')
    arq = config.get('planner','file').split(',')

    for a in arq:
        if tipo == 'xls':
            df = pd.read_excel(f'{base}\{dir}\{a}')
        dfa.append([a,df])
        
    return(dfa)


from fastapi import FastAPI
import pandas as pd
import json

def parse_plan(df):
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed

config = ConfigParser()
config.read("config.ini")
#print(config.sections())
base = config.get('arquivos','base')
dir = config.get('planner','dir')
tipo = config.get('planner','tipo')
arq = config.get('planner','file').split(',')

app = FastAPI()

lista_de_dfs = []

for i in arq:
    lista_de_dfs.append(parse_plan(pd.read_excel(f"{base}\{dir}\{i}")))

#print(lista_de_dfs)

@app.get("/dados")
def load_dados():
    return lista_de_dfs
    
#load server: python -m uvicorn planner:app --reload