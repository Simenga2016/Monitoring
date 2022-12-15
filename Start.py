# Сreating some starting conditions, like local database and tables

from Func import *
import Querey
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    connection = psycopg2.connect(user="postgres",
                                  password="1111",
                                  host="127.0.0.1",
                                  port="5432")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = 'create database main_Db' #DB creating
    cursor.execute(sql_create_database)
except (Exception, Error) as error:
    pass # if DB exist, this except make program continue
finally:
    if connection:
        cursor.close()
        connection.close() #Close connection to whole DB


#Connet co exist 'main_db' DB
DB = psycopg2.connect(database="main_db",
                      user="postgres",
                      password="1111",
                      host="127.0.0.1",
                      port="5432")

# Creating and Populating Database Names
try:
    execute_query(DB,Querey.create_type_table)
    execute_query(DB,Querey.create_settings_table)
    execute_query(DB,Querey.create_error_history_table)
    execute_query(DB,Querey.create_user_table)
except Error as e:
    print(e) # Just for safe, it shouldn't do something. It's for debugging
db_cursor = DB.cursor()
# Add to type:
sql_get_type ='''select * from type'''
db_cursor.execute(sql_get_type)
if not (db_cursor.fetchall()):
    types = ["'Опрос БД'", "'Ping сервера'", "'Опрос микро-сервиса'", "'Обращение к Nginx'"]
    for i in types:
        add_to_db(DB, 'type', 'name', i)

# Add to settings start lines TODO: add some examples here
db_cursor.execute('''Select * from settings ''')
if not(db_cursor.fetchall()):
    print('Empty settings!')