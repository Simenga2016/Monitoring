## Some functions for local SQLite DB

import os
import psycopg2
from psycopg2 import Error


def create_PostgreSQL_connection(db, user='postgres', password='1111', host='localhost', port=5432):
    connection = None
    try:
        connection = psycopg2.connect(database=db, user=user, password=password, host=host, port=port)
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
        pass
        # print(f"Execution error! {e}")


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


def create_postgreSQL_error_message():
    DB = create_PostgreSQL_connection('MainDB')
    cursor = DB.cursor()
    error_id = (cursor.execute('SELECT id FROM error_history ORDER BY id DESC LIMIT 1')).fetchall()[0][0]
    settings_id = \
        (cursor.execute('SELECT settings_id FROM error_history ORDER BY id DESC LIMIT 1')).fetchall()[0][0]
    error_time = (cursor.execute('SELECT error_time FROM error_history ORDER BY id DESC LIMIT 1')).fetchall()[0][
        0]
    project = cursor.execute(f'SELECT project FROM settings where id = {settings_id}').fetchall()[0][0]
    server = cursor.execute(f'SELECT server FROM settings where id = {settings_id}').fetchall()[0][0]
    type_id = cursor.execute(f'SELECT type FROM settings where id = {settings_id}').fetchall()[0][0]
    name = cursor.execute(f'SELECT name FROM type where id = {type_id}').fetchall()[0][0]
    message = f"!!!Внимание!!! Сбой в программном обеспечение!\n" \
              f"Error id: {error_id}\n" \
              f"Проект: {project}\n" \
              f"Служба: {name}\n" \
              f"Дата: {error_time}\n" \
              f"Server: {server}"
    return message

def add_to_history(error):
    error_history = create_PostgreSQL_connection("main_db")
    add_to_db(error_history, 'error_history', 'settings_id, error_time, log',
              f'{error["settings_id"]}, "{str(error["error_time"])}", "{error["log"]}"')

if __name__ == '__main__':
    print('What are you doing here?')