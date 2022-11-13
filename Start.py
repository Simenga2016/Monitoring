# Сreating some starting conditions, like local databases

from Func import *
import os
import Querey
import datetime

# Conneting to databases
type = create_connection(f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Type.sqlite")
settings = create_connection(f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Settings.sqlite")
error_history = create_connection(
    f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Error_history.sqlite")
telebot_users = create_connection(f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Users.sqlite")

# Populating Database Names
execute_query(type, Querey.create_type_table)
execute_query(settings, Querey.create_settings_table)
execute_query(error_history, Querey.create_error_history_table)
execute_query(telebot_users, Querey.create_user_table)

# Add to type:
cursor = type.cursor()
info = cursor.execute('SELECT * FROM type WHERE name="Ping сервера"')
if not (info.fetchone()):
    types = ["'Опрос БД'", "'Ping сервера'", "'Опрос микро-сервиса'", "'Обращение к Nginx'"]
    for i in types:
        add_to_db(type, 'type', 'name', i)

#Add to settings start lines
cursor = settings.cursor()
info = (cursor.execute("SELECT * FROM settings")).fetchall()
if not (info): #Add one request of each type to Settings if it's empty
    query = '"Server": "f0741017.xsph.ru","Port": 22,"Login": "f0741017_TestBD","Password": "f0741017_TestBD","DB" : "f0741017_TestBD","Query" : "SELECT * FROM test WHERE num<20","Tunel" : 1,"Tunel_pass" : "tufaecitak","Tunel_log" : "f0741017"'
    execute_query(settings,
                  f"INSERT INTO settings (type,server,query,time_limit,time_out,last_time,project) VALUES (1,'f0741017.xsph','{query}',10,1500,'{datetime.datetime.now()}','Test Project')")
    query = '"Server": "google.com","Count": 7'
    execute_query(settings,
                  f"INSERT INTO settings (type,server,query,time_limit,time_out,last_time,project) VALUES (2,'google','{query}',1,200,'{datetime.datetime.now()}','Test Google Project')")
    query = '"Server": "https://randomuser.me/api/"'
    execute_query(settings,
                  f"INSERT INTO settings (type,server,query,time_limit,time_out,last_time,project) VALUES (3,'randomuserapi','{query}',3,300"
                  f",'{datetime.datetime.now()}','Test API Project')")
    query = '"Server": "http://80.94.166.151/"'
    execute_query(settings,
                  f"INSERT INTO settings (type,server,query,time_limit,time_out,last_time,project) VALUES (4,'Государственный комитет по науке и технологиям Республики Беларусь','{query}',15,800"
                  f",'{datetime.datetime.now()}','Test Nginx Project')")
    query = '"Server": "WRONGf0741017.xsph.ru","Port": 22,"Login": "WRONGf0741017_TestBD","Password": "WRONGf0741017_TestBD","DB" : "WRONGf0741017_TestBD","Query" : "SELECT * FROM test WHERE num<20","Tunel" : 1,"Tunel_pass" : "tufaecitak","Tunel_log" : "f0741017"'
    execute_query(settings,
                  f"INSERT INTO settings (type,server,query,time_limit,time_out,last_time,project) VALUES (1,'f0741017.xsph','{query}',10,1200,'{datetime.datetime.now()}','Test Project')")
    query = '"Server": "WRONGgoogle.com","Count": 7'
    execute_query(settings,
                  f"INSERT INTO settings (type,server,query,time_limit,time_out,last_time,project) VALUES (2,'google','{query}',1,200,'{datetime.datetime.now()}','Test Google Project')")
    query = '"Server": "https://randomuser.me/api/WRONG"'
    execute_query(settings,
                  f"INSERT INTO settings (type,server,query,time_limit,time_out,last_time,project) VALUES (3,'WRONGrandomuserapi','{query}',3,300"
                  f",'{datetime.datetime.now()}','Test API Project')")
    query = '"Server": "http://80.94.166.151/WRONG"'
    execute_query(settings,
                  f"INSERT INTO settings (type,server,query,time_limit,time_out,last_time,project) VALUES (4,'Государственный комитет по науке и технологиям Республики Беларусь','{query}',15,800"
                  f",'{datetime.datetime.now()}','Test Nginx Project')")