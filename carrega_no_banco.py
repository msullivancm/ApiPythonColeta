from configparser import ConfigParser
import pandas as pd
import openpyxl
import sqlite3

class carga_no_banco():
    def __init__(self):
        self.conn = sqlite3.connect('kpis.db')
        self.cur = self.conn.cursor()

    def appendtocsv(self, tabela):
        if tabela == list:
            for t in tabela:
                data=pd.read_excel(tabela)
                data.to_csv(tabela+".csv",index=False,header=False,mode="a")
            
    def carga_excel_sqlite(self, tabela):
        if type(tabela)==list:
            wb = pd.DataFrame()
            for t in tabela:
                wb = pd.read_excel(t, sheet_name=None)
                wb.rename('Tarefas','Tarefas2')
                for sheet in wb:
                    try:
                        wb[sheet].to_sql(sheet,
                                 self.conn, 
                                 if_exists='fail')
                    except:
                        print("Erro na carga")
                self.conn.execute("CREATE UNIQUE INDEX Tarefas_Identificação_da_tarefa_IDX ON Tarefas ('Identificação da tarefa');")
                self.conn.commit()
                self.fechar()
    
    def execute_query(self, query):
        try:
            df = pd.read_sql(query, self.conn)
            self.cur(query)
            self.conn.commit()
            print("Query successful")
            return df
        except:
            print(f"Error: '{query}'")
            
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
        print(self.config.sections())
        
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

carga_no_banco().appendtocsv(obj.gera_caminho()) 


""" df = carga_no_banco().execute_query("INSERT INTO Tarefas ('Identificação da tarefa', 'Nome da tarefa') VALUES('teste2','sullivan2');")
print(df) """
            
