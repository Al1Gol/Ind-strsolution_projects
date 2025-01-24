import json
import psycopg2
import os

#from celery import shared_task
# Импорт проектов
class LoadProjects():
    def __init__(self):
        # Основная  директория
        self.worker_dir = None
        # Файл выгрузки
        self.export_path = None
        self.export_file=None
        # Файл фикстуры
        self.import_path=None
        self.import_file=None
        # Параметры подключения к БД
        self.dbname = None
        self.user = None
        self.password = None
        self.host = None

    def get_dict(self, id, contract, name, start_date, deadline, is_completed, actual_date, resp, resp_rp):
        dict_test = {
            "model": "projectsapp.projects",
            #"pk": id,
            "fields": {
                "contract_id": id,
                "name": name,
                "start_date":  start_date,
                "deadline": deadline,
                "is_completed": is_completed,
                "actual_date": actual_date,
                "responsible": resp,
                "responsible_rp": resp_rp
                }
        }
        return dict_test

    #
    def get_fixture(self):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, 
                                password=self.password, host=self.host)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM projectsapp_projects')
        conn.commit()
        cursor.execute('SELECT contract_number FROM projectsapp_contracts')
        records = [el[0] for el in cursor.fetchall()]

        # Переменная для записи в фикстуру
        fixture = []

        # Исходный файл состоит из списка словарей
        with open(f'{self.export_path}{self.export_file}', mode='r', encoding='utf-8-sig') as file:
            projects_dict = json.loads(file.read())
            projects_dict = projects_dict.get('tab')
            # Проходим по списку договоров
            for project in projects_dict:
                contract = project['Номер']
                name = project['Наименование'] if project['Наименование'] else None
                start_date = project['ДатаНачала'] if project['ДатаНачала'] else None
                deadline = project['СрокВыполнения'] if project['СрокВыполнения'] else None
                is_completed = project['Выполнено']
                actual_date = project['ДатаФактическогоВыполнения'] if project['ДатаФактическогоВыполнения'] else None
                resp = ''#project['Ответственный']
                resp_rp = ''#project['ОтветственныйРП']
                if contract in records:
                    cursor.execute('SELECT id FROM projectsapp_contracts where contract_number=%s', (contract, ))
                    id = cursor.fetchone()[0]
                    fixture.append(self.get_dict(id, contract, name, start_date, deadline, is_completed, actual_date, resp, resp_rp))
        return fixture
    
    def save(self):
        fixture=self.get_fixture()
        print(fixture)
        # Сохранение фикстуры
        with open(f'{self.import_path}{self.import_file}', mode='w+', encoding='utf-8') as file:
            json.dump(fixture, file, ensure_ascii=False, indent=4)

    def update_db(self):
	# Загрузка полученной фикстуры в приложение
        if os.name == 'nt':
            os.system('python -Xutf8 ./backend/indsol_web/manage.py loaddata projects.json --settings=indsol_web.settings.debug')
        else:
	        os.system(f'python -Xutf8 {self.worker_dir}/manage.py loaddata projects.json --settings=indsol_web.settings.pre_production')

# Импорт проектов
#from celery import shared_task
class LoadAdjustes():
    def __init__(self):
        # Основная  директория
        self.worker_dir = None
        # Файл выгрузки
        self.export_path = None
        self.export_file=None
        # Файл фикстуры
        self.import_path=None
        self.import_file=None
        # Параметры подключения к БД
        self.dbname = None
        self.user = None
        self.password = None
        self.host = None

    def get_dict(self, id, contract, subject, sent_date, recieve_date, is_agreed):
        dict_test = {
            "model": "projectsapp.adjust",
            #"pk": id,
            "fields": {
                "contract_id": id,
                "subject": subject,
                "sent_date":  sent_date,
                "recieve_date": recieve_date,
                "is_agreed": is_agreed
                }
        }
        return dict_test

    #
    def get_fixture(self):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, 
                                password=self.password, host=self.host)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM projectsapp_adjust')
        conn.commit()
        cursor.execute('SELECT contract_number FROM projectsapp_contracts')
        records = [el[0] for el in cursor.fetchall()]

        # Переменная для записи в фикстуру
        fixture = []

        # Исходный файл состоит из списка словарей
        with open(f'{self.export_path}{self.export_file}', mode='r', encoding='utf-8-sig') as file:
            adjustes_dict = json.loads(file.read())
            adjustes_dict = adjustes_dict.get('tab')
            # Проходим по списку договоров
            for adjust in adjustes_dict:
                contract = adjust['Номер']
                subject = adjust['ПредметСогласования'] if adjust['ПредметСогласования'] else None
                sent_date = adjust['ДатаОтправки'] if adjust['ДатаОтправки'] else None
                recieve_date = adjust['ДатаПолучения'] if adjust['ДатаПолучения'] else None
                is_agreed = adjust['Согласовано']
                if contract in records:
                    cursor.execute('SELECT id FROM projectsapp_contracts where contract_number=%s', (contract, ))
                    id = cursor.fetchone()[0]
                    fixture.append(self.get_dict(id, contract, subject, sent_date, recieve_date, is_agreed))
        return fixture
    
    def save(self):
        fixture=self.get_fixture()
        # Сохранение фикстуры
        with open(f'{self.import_path}{self.import_file}', mode='w+', encoding='utf-8') as file:
            json.dump(fixture, file, ensure_ascii=False, indent=4)

    def update_db(self):
	# Загрузка полученной фикстуры в приложение
        if os.name == 'nt':
            os.system('python -Xutf8 ./backend/indsol_web/manage.py loaddata adjust.json --settings=indsol_web.settings.debug')
        else:
            os.system(f'python -Xutf8 {self.worker_dir}/manage.py loaddata adjust.json --settings=indsol_web.settings.pre_production')



if __name__ == "__main__":
    projects =  LoadProjects()
    # Настройки БД
    projects.dbname='indsol_test'
    projects.user='postgres'
    projects.password='123'
    projects.host='localhost'
    # Настройка файлов
    # Файл выгрузки
    projects.export_path = './backend/media/parse_data/'
    projects.export_file= 'projects.json'
    # Файл фикстуры
    projects.import_path='./backend/indsol_web/projectsapp/fixtures/'
    projects.import_file='projects.json'

    projects.save()
    projects.update_db()

    adjustes =  LoadAdjustes()
    # Настройки БД
    adjustes.dbname='indsol_test'
    adjustes.user='postgres'
    adjustes.password='123'
    adjustes.host='localhost'
    # Настройка файлов
    # Файл выгрузки
    adjustes.export_path = './backend/media/parse_data/'
    adjustes.export_file= 'adjust.json'
    # Файл фикстуры
    adjustes.import_path='./backend/indsol_web/projectsapp/fixtures/'
    adjustes.import_file='adjust.json'

    adjustes.save()
    adjustes.update_db()

