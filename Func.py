## Some functions for local SQLite DB

import sqlite3
from sqlite3 import Error
import os


# Create connection to SQLite database
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"Connection error!  {e}")
    return connection


# Change of SQLite database
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"Execution error! {e}")


# Create sql-request to add new line into database
def create_insert_line(table, args, what):
    line = f"""
    INSERT INTO
      {table} ({args})
    VALUES
      ({what})  
"""
    return line


# Add line to database
def add_to_db(table, text_table, args, what):
    line = create_insert_line(text_table, args, what)
    execute_query(table, line)

#Create error message for last line in Error_history SQLite database
def create_error_message():
    type = create_connection(f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Type.sqlite")
    settings = create_connection(f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Settings.sqlite")
    error_history = create_connection(
        f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Error_history.sqlite")
    error_cursor = error_history.cursor()
    error_id = (error_cursor.execute('SELECT id FROM error_history ORDER BY id DESC LIMIT 1')).fetchall()[0][0]
    settings_id = \
        (error_cursor.execute('SELECT settings_id FROM error_history ORDER BY id DESC LIMIT 1')).fetchall()[0][0]
    error_time = (error_cursor.execute('SELECT error_time FROM error_history ORDER BY id DESC LIMIT 1')).fetchall()[0][
        0]
    settings_cursor = settings.cursor()
    project = settings_cursor.execute(f'SELECT project FROM settings where id = {settings_id}').fetchall()[0][0]
    server = settings_cursor.execute(f'SELECT server FROM settings where id = {settings_id}').fetchall()[0][0]
    type_id = settings_cursor.execute(f'SELECT type FROM settings where id = {settings_id}').fetchall()[0][0]
    type_cursor = type.cursor()
    name = type_cursor.execute(f'SELECT name FROM type where id = {type_id}').fetchall()[0][0]
    message = f"!!!Внимание!!! Сбой в программном обеспечение!\n" \
              f"Error id: {error_id}\n" \
              f"Проект: {project}\n" \
              f"Служба: {name}\n" \
              f"Дата: {error_time}\n" \
              f"Server: {server}"
    return message

#Send message to TG-bot //ToDo
def send_to_TG(message):
    print(message)

# Add error to Error_history SQLite DB
def add_to_history(error):
    error_history = create_connection(
        f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Error_history.sqlite")
    add_to_db(error_history, 'error_history', 'settings_id, error_time, log',
              f'{error["settings_id"]}, "{str(error["error_time"])}", "{error["log"]}"')
