from sqlalchemy import create_engine
import pymysql
import pandas as pd
import openpyxl 
import sys
from configparser import ConfigParser

#lê arquivo de configuração e carrega variáveis
config = ConfigParser()
config.read('gerarelatoriootrs.ini')
print(config.sections())
dbdriver=config.get('CONNECT','driver')
dbdatabase=config.get('CONNECT','database')
dbssl=config.get('CONNECT','ssl')
dbhost=config.get('CONNECT','host')
dbuser=config.get('CONNECT','user')
dbpass=config.get('CONNECT','pass')
dbsslca=config.get('CONNECT','ssl_ca')
dbsslkey=config.get('CONNECT','ssl_key')
dbsslcert=config.get('CONNECT','ssl_cert')
dir_destino =config.get('DIR','target')

if dbssl=='True':
    db_connection_str = f'{driver}+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbdatabase}'
    db_ssl_args = {'ssl_ca': dbsslca,
                'ssl_key': dbsslkey,
                'ssl_cert': dbsslcert}
    db_connection = create_engine(db_connection_str, connect_args=db_ssl_args)
else: 
    db_connection_str = f'{dbdriver}+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbdatabase}'
    db_connection = create_engine(db_connection_str)

query = """SELECT
        t.id,
        t.TN AS 'Numero do Ticket',
        ts.name Status,
        t.TITLE AS Titulo,
        q.name AS Fila,
        t.CREATE_TIME AS Dt_Criacao_Ticket,
        t.customer_id AS username,
        CONCAT(u.first_name, ' ', u.last_name) AS Analista,
        (select 
                case sv2.vote_value
                        when 1 then '1 - Muito Insatisfeito'
                        when 2 then '2 - Insatisfeito'
                        when 3 then '3 - Regular'
                        when 4 then '4 - Satisfeito'
                        when 5 then '5 - Muito Satisfeito'
                        ELSE 'Não respondido'
                end
        from
                        survey_vote sv2
        inner join survey_request sr2 on
                        sv2.request_id = sr2.id
        inner join ticket t2 on
                        sr2.ticket_id = t2.id
        where
                        sv2.question_id = 2 #Satisfacao
                and t2.id = t.id limit 1) as Satisfacao,
        case
                when sla.solution_time is null then 'SIM'
                when sla.solution_time * 60 >= TIME_TO_SEC(dfv.value_text) then 'SIM'
                else 'NÂO'
        end as 'Dentro do SLA',
        SEC_TO_TIME(sla.solution_time * 60) as SLA,
    dfv.value_text as TPA,
        (select  
                        case
                                when max(SUBSTRING(sv2.vote_value, 12)) <> '' then max(SUBSTRING(sv2.vote_value, 12))
                        else 'Não respondido'
                end
        from
                        survey_vote sv2
        inner join survey_request sr2 on
                        sv2.request_id = sr2.id
        inner join ticket t2 on
                        sr2.ticket_id = t2.id
        where
                        sv2.question_id = 3 #Comentario
                and t2.id = t.id LIMIT 1) as Comentario,
        datediff(now(),t.create_time) Aging
FROM
                ticket t
Left join users u ON
                t.user_id = u.id
Left join queue q ON
                q.id = t.queue_id
left join sla on
                sla.id = t.sla_id
left join ticket_history th on
                th.id = t.id
left join ticket_state ts on
        ts.id = t.ticket_state_id
left join dynamic_field_value dfv on t.id = dfv.object_id
left join dynamic_field df on dfv.field_id = df.id  """

df = pd.read_sql(query, con=db_connection)

df.to_excel(dir_destino+'/ChamadosOTRS.xlsx', index=False)