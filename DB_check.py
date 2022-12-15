# Create DB and populating them, some var's for local DB
from Start import *

from json import loads
from sshtunnel import SSHTunnelForwarder
import MySQLdb
from MySQLdb import Error, MySQLError
import multiprocessing


def create_tunnel(adres, port, passwd, user):
    try:
        tunnel = SSHTunnelForwarder(
            (f'{adres}', int(f'{port}')),
            ssh_password=f'{passwd}',
            ssh_username=f'{user}',
            remote_bind_address=('localhost', 3306)
        )
        return tunnel
    except Error as e:
        return str(e)


# For mySQL
def create_connection(user, passwd, db, port):
    try:
        if isinstance(port, SSHTunnelForwarder):
            connection = MySQLdb.connect(user=f'{user}', passwd=f'{passwd}', db=f'{db}',
                                         host='127.0.0.1', port=port.local_bind_port)
        else:
            connection = MySQLdb.connect(user=f'{user}', passwd=f'{passwd}', db=f'{db}',
                                         host='127.0.0.1', port=port)
        return connection
    except Error as e:
        return str(e)


def create_execution(connect, quote):
    try:
        cursor = connect.cursor()
        cursor.execute(quote)
        return cursor
    except Error as e:
        return str(e)


def Connect_and_execute(query_settings, server, queue):
    if 'Tunel' in query_settings.keys() and query_settings["Tunel"]:
        tunel = create_tunnel(server, 22, query_settings["Tunel_pass"], query_settings["Tunel_log"])
        if isinstance(tunel,str):
            queue.put(tunel)
            return
        try:
            tunel.start()
        except Exception as e:
            queue.put(str(e))
            return
        connection = create_connection(query_settings['Login'], query_settings['Password'],
                                       query_settings['DB'],
                                       tunel)
    else:
        connection = create_connection(query_settings['Login'], query_settings['Password'],
                                       query_settings['DB'],
                                       query_settings['port'])

    if (isinstance(connection, str)):
        queue.put(connection)
        return

    execution = create_execution(connection, query_settings["Query"])
    if (isinstance(execution, str)):
        queue.put(execution)
        return

    queue.put(None)


def create_time_error_db_message(settings_id, datatime, server):
    message = f"Запрос к базе данных {server}: \n" \
              f"Превышен предел времени ожидания! \n"
    error_message = {"settings_id": settings_id, "error_time": datatime, "log": message}
    return (error_message)


def create_some_error_db_message(settings_id, datatime, server, text):
    message = f"Запрос к базе данных {server}: \n" \
              f"{text} \n"
    error_message = {"settings_id": settings_id, "error_time": datatime, "log": message}
    return (error_message)


# Main function of this file. Return list or errors
def Get_DB_Check():
    Error_messages = []
    settings_info = settings.execute('SELECT * FROM Settings WHERE type=1')

    for base in settings_info:
        try:
            if ((datetime.datetime.now() - datetime.datetime.strptime(base[6], '%Y-%m-%d %H:%M:%S.%f')).seconds > base[
                4] * 60) or (
                    (datetime.datetime.now() - datetime.datetime.strptime(base[6], '%Y-%m-%d %H:%M:%S.%f')).days):
                query_settings = loads('{' + base[3] + '}')
                timeout = base[5] / 1000
                queue = multiprocessing.Queue()
                p = multiprocessing.Process(target=Connect_and_execute(query_settings, query_settings['Server'], queue))
                p.start()
                p.join(timeout)
                flag = 0
                if p.is_alive():
                    flag = 1
                e = queue.get()
                if e:
                    Error_messages.append(create_some_error_db_message(base[0], datetime.datetime.now(), base[2], str(e)))
                elif flag == 1:
                    Error_messages.append(create_time_error_db_message(base[0], datetime.datetime.now(), base[2]))
                if flag == 1:
                    p.kill()
                p.join()
                execute_query(settings,
                              f"UPDATE settings SET last_time = '{datetime.datetime.now()}' WHERE id = {base[0]}")
        except MySQLError as e:
            print(1)
            Error_messages.append(create_some_error_db_message(base[0], datetime.datetime.now(), base[2], e))

    return Error_messages


if __name__ == '__main__':
    print(Get_DB_Check())
