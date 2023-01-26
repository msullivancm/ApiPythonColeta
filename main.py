# main.py
from fastapi import FastAPI
import pandas as pd
import os
from typing import Union

origem = r"C:\Users\eu_uv\OneDrive\MeusDocumentos\Clientes\Ferroport\TI\KPIs da TI\AutomacaoKPIsPowerBI"

app = FastAPI()
@app.get("/")
async def root():
    return {"ApiDeColetaDeDados":"by Marcus Sullivan"}

@app.get("/items/{dt_criacao}")
async def read_item(dt_criacao: str, q: Union[str, None] = None, short: bool = False):
    dt_criacao = {"dt_criacao": dt_criacao}
    from consultaotrscloud import consultaOtrsCloud
    return f'{"Retorno": {dt_criacao}}'
    #return consultaOtrsCloud(dt_criacao)
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#Exemplo: http://127.0.0.1:8000/items/foo?short=true

'''@app.get("/otrscloud/{dt_criacao}")
async def otrscloud(dt_criacao: str | None = None):
    from consultaotrscloud import consultaOtrsCloud
    return f'{"Retorno": {dt_criacao}}'
    #return consultaOtrsCloud(dt_criacao)'''
    
'''@app.get("/impressao")
async def impressao():'''
def impressao():
    df=pd.DataFrame()
    pasta = origem + '\impressao'
    primeiro = True
    arqtemp=''
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            temp=os.path.join(os.path.realpath(diretorio), arquivo)
            if '.csv' in temp:
                if primeiro:
                    print(pd.read_csv(temp),sep='LF')
                    #df.to_csv(arqtemp, index=False,header=True)
                    primeiro=False
                else:
                    pass 
                    #df.to_csv(arqtemp, index=False,header=False,mode="a")
    return df

print(impressao())

#Iniciar servidor: python -m uvicorn main:app --reload