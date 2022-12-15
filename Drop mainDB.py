import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="1111")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    # Создайте курсор для выполнения операций с базой данных
    cursor = connection.cursor()

    # Выполнение команды: это создает новую таблицу
    cursor.execute("drop database main_db")
    connection.commit()
    print("БД успешно удалена в PostgreSQL")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")