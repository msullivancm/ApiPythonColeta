from configparser import ConfigParser
import pandas as pd
import openpyxl
import sqlite3

class carga_no_banco():
    def __init__(self):
        self.conn = sqlite3.connect('kpis.db')
        self.cur = self.conn.cursor()

    def carga_excel_sqlite(self, tabela):
        finalexcelsheet = pd.DataFrame()
        if type(tabela)==list:
            for t in tabela:
                wb = pd.read_excel(t, sheet_name=None)
                for sheet in wb:
                    wb[sheet].to_sql(sheet,self.conn, index=False, if_exists='append')
                    self.conn.commit()
                self.conn.close()
        else:
            wb = pd.read_excel(tabela, sheet_name=None)
            for sheet in wb:
                wb[sheet].to_sql(sheet,self.conn, index=False, if_exists='append')
                self.conn.commit()
            self.fechar()
            
    def fechar(self):
        self.cur.close()
        self.conn.close()
        
class Coleta():
    def __init__(self, *args):
        #print(args)
        self.sessao1 = args[0]
        self.sessao2 = args[1]
        self.base = args[2]
        self.item_dir = args[3]
        self.item_tipo = args[4]
        self.item_file = args[5]
    
        self.config = ConfigParser()
        self.config.read("config.ini")
        #print(self.config.sections())
        
        self.nome_arquivo=[]
        self.lista_de_dataframes=[]
        self.diretorio_base = self.config.get(self.sessao1,self.base)
        self.dir = self.config.get(self.sessao2,self.item_dir)
        self.tipo = self.config.get(self.sessao2,self.item_tipo)
        self.arq = self.config.get(self.sessao2,self.item_file).split(',')

    def gera_caminho(self):
        lista_caminho=[]
        for i in self.arq:
            lista_caminho.append(f'{self.diretorio_base}\{self.dir}\{i}')
        return lista_caminho
    
obj = Coleta('arquivos', 'planner', 'base', 'dir', 'tipo', 'file')
for file in obj.gera_caminho():
    carga_no_banco().carga_excel_sqlite(file)

