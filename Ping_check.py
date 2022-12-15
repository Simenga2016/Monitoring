import pythonping
from json import loads
import datetime
from Func import *


def create_error_message(settings_id, datatime, server, error):
    message = f"Обмен пакетами с [{server}]: \n" \
              f"{error}"
    error_message = {"settings_id": settings_id, "error_time": datatime, "log": message}
    return (error_message)


def create_ping_error_message(settings_id, datatime, server, data):
    send = 0
    lost = 0
    taked = 0
    string = ''
    for i in data:
        string += str(i) + '\n'
        send += 1
        if str(i) == 'Request timed out':
            lost += 1
        else:
            taked += 1

    message = f"Обмен пакетами с [{server}]: \n" \
              f"{string}\n" \
              f"Статистика для {server}:\n" \
              f"Пакетов: отправлено = {send}, получено = {taked}, потеряно = {lost}" \
              f"({round(lost / send * 100)}% потерь)"
    error_message = {"settings_id": settings_id, "error_time": datatime, "log": message}
    return (error_message)


def Ping_check():
    Error_messages = []

    DB = psycopg2.connect(database="main_db",
                          user="postgres",
                          password="1111",
                          host="127.0.0.1",
                          port="5432")
    # settings_info = settings.cursor().execute('SELECT * FROM Settings WHERE type=2')
    cursor = DB.cursor()
    cursor.execute('SELECT * FROM Settings WHERE type=2')

    for serv in (cursor.fetchall()):
        # print(serv)
        if ((datetime.datetime.now() - datetime.datetime.strptime(str(serv[6]), '%Y-%m-%d %H:%M:%S.%f')).seconds > serv[
            4] * 60) or ((datetime.datetime.now() - datetime.datetime.strptime(str(serv[6]), '%Y-%m-%d %H:%M:%S.%f')).days):
            query_settings = serv[3]
            timeout = serv[5] / 1000
            try:
                res = pythonping.ping(query_settings['Server'], count=query_settings['Count'], timeout=timeout)
            except Exception as e:
                Error_messages.append(create_error_message(serv[0], datetime.datetime.now(), serv[2], e))
            if (res.stats_success_ratio != 1):
                Error_messages.append(create_ping_error_message(serv[0], datetime.datetime.now(), serv[2], res))
            execute_query(DB, f"UPDATE settings SET last_time = '{datetime.datetime.now()}' WHERE id = {serv[0]}")
    return (Error_messages)


if __name__ == '__main__':
    Mes = Ping_check()
    print('|__|')
    for i in Mes:
        print(i)
