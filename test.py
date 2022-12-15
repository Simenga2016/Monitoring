import json

import psycopg2
from psycopg2 import Error
from Func import *
import datetime
from json import loads, load

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="1111",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="main_db")

    # Создайте курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # SQL-запрос для создания новой таблицы
    query = '{"Server": "b2b.sellwin.by"}'
    json_settings = json.loads(query)
    sql_add = f'''
            INSERT INTO
      settings (type,server,query,time_limit,time_out,last_time,project)
    VALUES
      (4,'Sellwin','{query}',15,800,'{datetime.datetime.now()}','Test Selwin Project')
'''
    cursor.execute(sql_add)
    connection.commit()
    # query = '"Server": "f0741017.xsph.ru","Port": 22,"Login": "f0741017_TestBD","Password": "f0741017_TestBD","DB" : "f0741017_TestBD","Query" : "SELECT * FROM test WHERE num<20","Tunel" : 1,"Tunel_pass" : "tufaecitak","Tunel_log" : "f0741017"'
    # add_to_db(connection, 'settings', "(type,server,query,time_limit,time_out,last_time,project)",
    #           f"(1,'f0741017.xsph','{query}',10,1500,'{datetime.datetime.now()}','Test Project')")
    create_table_query = """
SELECT * FROM Settings WHERE type=2
"""
    cursor.execute('SELECT * FROM Settings WHERE type=3')
    print(cursor.fetchall())
    cursor.execute(create_table_query)
    # cursor.fetchall()
    for i in (cursor.fetchall()):
        print(i)

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
