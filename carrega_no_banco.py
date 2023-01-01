from configparser import ConfigParser
import pandas as pd
import openpyxl
import sqlite3

class carga_no_banco():
    def __init__(self):
        self.conn = sqlite3.connect('kpis.db')
        self.cur = self.conn.cursor()
    
    def cria_tabela(self, tabela):
        query = f"create or replace table {tabela};"
        resultado = self.cur(query)
        return resultado
    
    def carrega_tabela():
        query = f""
        resultado = self.cur(query)
        return resultado
    
    def fechar():
        self.cur.close()
        self.conn.close()
        
class Coleta():
    def __init__(self, *args):
        print(args)
        self.sessao1 = args[0]
        self.sessao2 = args[1]
        self.base = args[2]
        self.item_dir = args[3]
        self.item_tipo = args[4]
        self.item_file = args[5]
    
        self.config = ConfigParser()
        self.config.read("config.ini")
        print(self.config.sections())
        
        self.nome_arquivo=[]
        self.lista_de_dataframes=[]
        self.diretorio_base = self.config.get(self.sessao1,self.base)
        self.dir = self.config.get(self.sessao2,self.item_dir)
        self.tipo = self.config.get(self.sessao2,self.item_tipo)
        self.arq = self.config.get(self.sessao2,self.item_file).split(',')

    #for a in arq:
     #   if tipo == 'xls':
            #df = pd.read_excel(f'{base}\{dir}\{a}')
        #dfa.append([a,df])
        
    #return(dfa)
    def gera_caminho(self):
        lista_caminho=[]
        for i in self.arq:
            lista_caminho.append(f'{self.diretorio_base}\{self.dir}\{i}')
        return lista_caminho
    
obj = Coleta('arquivos', 'planner', 'base', 'dir', 'tipo', 'file')
print(obj.gera_caminho()) #gera uma lista de caminhos

openpyxl.open(filename)