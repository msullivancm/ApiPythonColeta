# main.py
from fastapi import FastAPI
import pandas as pd
import os

origem = r"C:\Users\eu_uv\OneDrive\MeusDocumentos\Clientes\Ferroport\TI\KPIs da TI\AutomacaoKPIsPowerBI"

app = FastAPI()
@app.get("/")
async def root():
    return {"ApiDeColetaDeDados":"by Marcus Sullivan"}

@app.get("/otrscloud")
async def otrscloud():
    from consultaotrscloud import consultaOtrsCloud
    return consultaOtrsCloud()
    
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