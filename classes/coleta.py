import pandas as pd
import openpyxl

class Coleta():
    def __init__(self, base, dir, tipo, arqnames):
        self.base = base
        self.dir = dir
        self.tipo = tipo
        self.arqnames = arqnames
        
    def coleta(self):
        if type(self.arqnames) == list:
            for a in self.arqnames:
                if self.tipo == 'xls':
                    df = pd.read_excel(f'{base}\{dir}\{a}')
                dfa.append([a,df])
            return(dfa)
        else: 
            if self.tipo == 'xls':
                df = pd.read_excel(f'{base}\{dir}\{self.arqnames}')
                return(df)
        
    def imprime(self):
        print(self.base, self.dir, self.tipo, self.arqnames)
        print(self.coleta())

'''obj = Coleta('base', 'dir', 'tipo', 'arqnames')
obj.imprime()'''