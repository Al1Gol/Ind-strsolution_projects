СИСТЕМА УПРАВЛЕНИЯ ПРОЕКТАМИ

УСТАНОВКА:

    Для установки зависимостей из корня проекта запустить команду:
    pip install -r ./requirements.txt

    DEBUG РЕЖИМ:

    Установите PostgreSQL. 
    Для подключения к БД используется пользователь postgres с паролем 123. Создайте базу данных с имененм indsol_test.
    Изменить параметры подключения можно в файле ./indsol_web/indsol_web/settings/debug.py

    Миграция базы:
        python .\indsol_web\manage.py migrate --settings=indsol_web.settings.debug

    Создание учетной записи администратора:
        python .\indsol_web\manage.py createsuperuser

    