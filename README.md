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

    PRODUCTION РЕЖИМ:

    Установите PostgreSQL. 
    Для подключения к БД используется пользователь postgres с паролем 123. Создайте базу данных с имененм indsol.
    Изменить параметры подключения можно в файле ./indsol_web/indsol_web/settings/production.py

    Миграция базы:
        python .\indsol_web\manage.py migrate --settings=indsol_web.settings.production

    Создание учетной записи администратора:
        python .\indsol_web\manage.py createsuperuser

    #Запуск проекта в debug режиме
        python .\indsol_web\manage.py runserver --settings=indsol_web.settings.debug   
    
    #Запуск тестов
        python .\indsol_web\manage.py test --settings=indsol_web.settings.debug indsol_web/
