1. Что это?

Это приложение - тестовое задание Тразанова Н.С. для SellwinGroup. Для запуска необходимо запустить файл init.py. Все остальные файлы с разрешением .py необходимы для работы приложения.

2. Использование баз данных

Приложение работает, используя 4 базы данных (БД) SQLite:
    — Type - сохраненные типы проверок.
    — Settings - настройки различных соединений, соответствующих типам
    — Error_history - история сохраненных ошибок для уточнения произошедшего
    — Users - список id пользователей Telegram, которым нужно отправить сообщения об ошибках

Базовый вариант этих БД содержится в программе, при этом если при запуске будет отсутствовать файл "Settings.sqlite" система создаст его и прочие отсутствующие БД, заполнив их простыми примерам.

Базовый вариант файла Settings.sqlite имеет в себе по два примера для каждого типа проверок, верный и содержащий ошибку:
    — Проверка БД, находящейся на sprinthost.ru
    — Проверка пинга сервера Google
    — Проверка доступности randomuser api
    — Проверка сайта "Государственного комитета по науке и технологиям Республики Беларусь", находящегося на Nginx

Для проверки БД можно использовать два режима: прямого подключения, работающий по-умолчанию, и режим подключения через SSH-туннель, для чего в поле "query" необходимо добавить следующие поля:
    "Tunel" : 1 - Указатель необходимости использовать SSH-туннель
    "Tunel_pass" : "pass" - Пароль SSH-туннеля
    "Tunel_log" : "login" - Имя пользователя SSH-туннеля

3. Сообщения об ошибках

Приложение обрабатывает четыре типа опросов:
    — Произвольный запрос к БД, получаемый из раздела "query" файла Settings.sqlite
    — Ping-запрос к серверу
    — Get-запрос к произвольному Rest-подобному API и получение ответа сервера
    — Get-запрос к произвольному Nginx серверу и получение ответа сервера

При этом если результаты этих опросов не соответствуют ожиданиям, т.е. имеются ошибки, они сохраняются в БД Error_history и отправляются пользователю (см. 4)

4. Telegram

При запуске приложения после действий из пункта 2 запускается Telegram бот @SellwingroupMonitorBot.
До получения первого сообщения будет запущен "режим регистрации", во время которого бот при получении сообщения от любого пользователя запомнит его id и добавит его в БД Users.
После будет запущен 'режим сообщений', в котором всем пользователям из БД users будут отправляться сообщения об ошибках из пункта 3.

5. Заключение

Так, для проверки работоспособности приложения достаточно запустить файл init.py и написать боту @SellwingroupMonitorBot в течение полуминуты после этого. Для проверки собственных БД, северов, api или Nginx необходимо добавить соответствующие поля в локальную БД Settings.sqlite

__________________________

1. What is this?

This application is a test task of Trazanov N.S. for SellwinGroup. The init.py file must be run in order to run it. All other files with .py permission are necessary for running the application.

2. Using databases

The application works using 4 SQLite databases:
    - Type - saved check types.
    - Settings - settings of the different connections that correspond to types.
    - Error_history - history of saved errors to clarify what happened
    - Users - list of Telegram users id to send error messages to

The basic version of these databases is contained in the program, and if the "Settings.sqlite" file is missing at startup, the system will create it and other missing databases by filling them with simple examples.

The basic version of the Settings.sqlite file has two examples for each type of check, one true and one with an error:
    - Checking the database, located at sprinthost.ru
    - Checking Google server ping
    - Checking the availability of randomuser api
    - Checking the site "State Committee on Science and Technology of the Republic of Belarus", located on Nginx

To check the database you can use two modes: direct connection, which works by default, and the connection mode through an SSH-tunnel, for which you need to add the following fields to the "query" field:
    "Tunel" : 1 - Specify the need to use the SSH-tunnel
    "Tunel_pass" : "pass" - The password of the SSH-tunnel
    "Tunel_log" : "login" - Username of SSH-tunnel

3. Error messages

The application processes four types of polls:
    - Arbitrary query to the database, obtained from the "query" section of the Settings.sqlite file
    - Ping-query to the server
    - Get-request to arbitrary Rest-like API and getting server's response
    - Get-request to arbitrary Nginx server and get the server response

If the results of these queries are not as expected, i.e. there are errors, they are stored in the Error_history database and sent to the user (see 4.)

4. Telegram

When launching the application after the actions from step 2, the Telegram bot @SellwingroupMonitorBot is launched.
Before the first message will run "registration mode", during which the bot when receiving a message from any user will remember his id and add it to the database Users.
After that the 'message mode' will be started, during which all users from the Users database will be sent error messages from point 3.

5. Conclusion

So, to test if the application is working, all you need to do is run the init.py file and write to the @SellwingroupMonitorBot within half a minute after that. To test your own databases, servers, api or Nginx, you need to add the appropriate fields to your local database Settings.sqlite

Translated with www.DeepL.com/Translator (free version)