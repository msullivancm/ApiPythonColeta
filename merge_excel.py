import sqlite3
import pandas as pd

# coding: utf-8

#from __future__ import unicode_literals
import xlrd
import codecs

def output_insert_sqls(excel_path, output_path, sheet_names, table_names):
    book = xlrd.open_workbook(excel_path)
    out_f = codecs.open(output_path, "w", "utf_8")

    for i, sheet_name in enumerate(sheet_names):
        table_name = table_names[i]
        sheet = book.sheet_by_name(sheet_name)

        column_list = []
        for col in range(sheet.ncols):
            column_list.append(sheet.cell(0, col).value)

        sql_prefix = "INSERT INTO %s(%s) VALUES(" % (table_name, ",".join(column_list))
        sql_suffix = ");\n"

        for row in range(sheet.nrows):
            if row >= 1:
                value_list = []
                for col in range(sheet.ncols):
                    val = sheet.cell(row, col).value
                    if type(val) != float:
                        val = "'%s'" % (val,)
                    else:
                        val = str(val).replace(".0", "") 
                    value_list.append(val)
                sql = "%s%s%s" % (sql_prefix, ",".join(value_list), sql_suffix,)
                out_f.write(sql)
    out_f.close()


base=r"P:\MeusDocumentos\Clientes\Ferroport\TI\KPIs da TI\AutomacaoKPIsPowerBI"
dir="planner"
tipo="xls"
file="TI_Sistemas.xlsx,TI_Infraestrutura.xlsx"

conn = sqlite3.connect("kpis.db")
cursor = conn.cursor()
pbase = base
pbasedir = base + "\\" + dir
pfile = file.split(',')

primeiro=True
for i in pfile:
    caminho = pbasedir+"\\"+i
    df = pd.read_excel(caminho)
    if primeiro:
        df.to_csv(pbasedir+"\\"+"unificado.csv", encoding='utf-8-sig',index=False,header=True)
        primeiro=False
    else: 
        df.to_csv(pbasedir+"\\"+"unificado.csv", encoding='utf-8-sig',index=False,header=False,mode="a")
""" dftoexcel = pd.read_csv(pbasedir+"\\"+"unificado.csv")
dftoexcel.to_excel(pbasedir+"\\"+"unificado.xlsx", index=False)
dftoexcel.to_sql('unificado', conn) """
""" dftosql = pd.read_csv(pbasedir+"\\"+"unificado.csv")
dftosql.to_sql('unificado', conn, if_exists='append') """

output_insert_sqls(pbasedir, pbasedir, pfile[0], pfile)
