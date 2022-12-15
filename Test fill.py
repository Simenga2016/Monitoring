import json

import psycopg2
from psycopg2 import Error
from Func import *
import datetime
from json import loads, load

try:
    connection = psycopg2.connect(user="postgres",

                                  password="1111",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="main_db")
    cursor = connection.cursor()

    # Nginx and API add. Function return only errors, so i make them by hands

    query = '{"Server": "b2b.sellwin.by"}'
    json_settings = json.loads(query)
    sql_add = f'''
            INSERT INTO
      settings (type,server,query,time_limit,time_out,last_time,project)
    VALUES
      (4,'Sellwin1','{query}',15,800,'{datetime.datetime.now()}','Test Sellwin1 Project')
'''
    cursor.execute(sql_add)

    query = '{"Server": "https://nest.sellwin.by/tests/get-monitoring-info"}'
    json_settings = json.loads(query)
    sql_add = f'''
                INSERT INTO
          settings (type,server,query,time_limit,time_out,last_time,project)
        VALUES
          (3,'Sellwin2','{query}',15,800,'{datetime.datetime.now()}','Test Sellwin2 Project')
    '''
    cursor.execute(sql_add)

    query = '{"Server": "https://pm-api.sellwin.by/tests/get-monitoring-info"}'
    json_settings = json.loads(query)
    sql_add = f'''
                INSERT INTO
          settings (type,server,query,time_limit,time_out,last_time,project)
        VALUES
          (3,'Sellwin3','{query}',15,800,'{datetime.datetime.now()}','Test Sellwin3 Project')
    '''
    cursor.execute(sql_add)

    query = '{"Server": "pmlogistic.sellwin.by"}'
    json_settings = json.loads(query)
    sql_add = f'''
                INSERT INTO
          settings (type,server,query,time_limit,time_out,last_time,project)
        VALUES
          (4,'Sellwin','{query}',15,800,'{datetime.datetime.now()}','Test Sellwin4 Project')
    '''
    cursor.execute(sql_add)

    query = '{"Server": "beautyhouse.by"}'
    json_settings = json.loads(query)
    sql_add = f'''
                INSERT INTO
          settings (type,server,query,time_limit,time_out,last_time,project)
        VALUES
          (4,'Sellwin','{query}',15,800,'{datetime.datetime.now()}','Test Sellwin5 Project')
    '''
    cursor.execute(sql_add)
    connection.commit() # All Api and Nginx test values

    #Ping
    query = '{"Server": "172.16.0.87","Count": 5}'
    json_settings = json.loads(query)
    sql_add = f'''
                INSERT INTO
          settings (type,server,query,time_limit,time_out,last_time,project)
        VALUES
          (2,'Sellwin','{query}',15,800,'{datetime.datetime.now()}','Test Sellwin6 Project')
    '''
    cursor.execute(sql_add)

    query = '{"Server": "172.16.0.86","Count": 5}'
    json_settings = json.loads(query)
    sql_add = f'''
                INSERT INTO
          settings (type,server,query,time_limit,time_out,last_time,project)
        VALUES
          (2,'Sellwin','{query}',15,800,'{datetime.datetime.now()}','Test Sellwin7 Project')
    '''
    cursor.execute(sql_add)

    query = '{"Server": "172.16.0.84","Count": 5}'
    json_settings = json.loads(query)
    sql_add = f'''
                INSERT INTO
          settings (type,server,query,time_limit,time_out,last_time,project)
        VALUES
          (2,'Sellwin','{query}',15,800,'{datetime.datetime.now()}','Test Sellwin8 Project')
    '''
    cursor.execute(sql_add)

    connection.commit() # All Ping commit




except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
