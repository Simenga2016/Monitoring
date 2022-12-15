import telebot
from time import sleep
from DB_check import Get_DB_Check
from Ping_check import Ping_check
from REST_check import Rest_check
from json import loads
from Func import *

from Start import *

if __name__ == '__main__':

    # After launching this application, you should write to the @SellwingroupMonitorBot to register.
    # It is enough to do it only once.
    # After 60s or first message registration will be closed
    # In the future, all registered users will receive error messages while the program is running.

    bot = telebot.TeleBot('5572897114:AAGxwP9x0iYeE73hv1aKIqpYcrw0kl56M8c')


    telebot_users = psycopg2.connect(database="main_db",
                      user="postgres",
                      password="1111",
                      host="127.0.0.1",
                      port="5432")
    cursor = telebot_users.cursor()
    users = cursor.execute('SELECT user_id FROM user').fetchall()

    print('Start')
    while 1:

        Errors_to_send = []

        # Checking DB errors:

        DB_errors = Get_DB_Check()

        if DB_errors:
            for error in DB_errors:
                error["log"] = error["log"].replace('"', '')
                add_to_history(error)
                Errors_to_send.append(create_postgreSQL_error_message())

        # Checking site-ping errors:

        Ping_errors = Ping_check()

        if Ping_errors:
            for error in Ping_errors:
                error["log"] = error["log"].replace('"', '')
                add_to_history(error)
                Errors_to_send.append(create_postgreSQL_error_message())

        # Checking REST API errors:
        # Maybe I do not understand the task, but getting an error from the API and the Nginx server has a common solution, so I combined them
        # So, it's also Checking Nginx errors:

        API_errors = Rest_check()

        if API_errors:
            for error in API_errors:
                error["log"] = error["log"].replace('"', '')
                add_to_history(error)
                Errors_to_send.append(create_postgreSQL_error_message())

        for user in users:
            for error in Errors_to_send:
                try:
                    bot.send_message(f'{user[0]}', f'{error}')
                except:
                    pass
                sleep(1)
        sleep(10)
