import requests
from requests import RequestException
import datetime
from json import loads
from Func import *


def create_api_error_message(settings_id, datatime, server, code):
    message = f"Запрос к api {server}: \n" \
              f"Обнаружена ошибка с кодом {code} \n"
    error_message = {"settings_id": settings_id, "error_time": datatime, "log": message}
    return (error_message)


def create_api_time_error_message(settings_id, datatime, server):
    message = f"Запрос к api {server}: \n" \
              f"Превышен предел времени ожидания!\n"
    error_message = {"settings_id": settings_id, "error_time": datatime, "log": message}
    return (error_message)


def Rest_check():
    Error_messages = []

    settings = create_connection(f"{os.path.abspath(__file__).replace(os.path.basename(__file__), '')}/Settings.sqlite")
    settings_info = settings.execute('SELECT * FROM Settings WHERE type=3 OR type=4')

    for api in settings_info:
        if ((datetime.datetime.now() - datetime.datetime.strptime(api[6], '%Y-%m-%d %H:%M:%S.%f')).seconds > api[
            4] * 60) or (
                (datetime.datetime.now() - datetime.datetime.strptime(api[6], '%Y-%m-%d %H:%M:%S.%f')).days):
            query_settings = loads('{' + api[3] + '}')
            timeout = api[5] / 1000
            URL = str(query_settings['Server'])
            try:
                request = requests.get(URL, timeout=timeout)
                if not (request):
                    Error_messages.append(
                        create_api_error_message(api[0], datetime.datetime.now(), api[2], request.status_code))
            except RequestException:
                Error_messages.append(create_api_time_error_message(api[0], datetime.datetime.now(), api[2]))
            execute_query(settings, f"UPDATE settings SET last_time = '{datetime.datetime.now()}' WHERE id = {api[0]}")
    return (Error_messages)


if __name__ == '__main__':
    print(Rest_check())
