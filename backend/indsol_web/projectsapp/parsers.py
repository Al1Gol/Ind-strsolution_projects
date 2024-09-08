import json
import psycopg2
import os

#from celery import shared_task
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

    def get_dict(self, id, contract, todo, resp, resp_rp):
        dict_test = {
            "model": "projectsapp.projects",
            #"pk": id,
            "fields": {
                "contract_id": id,
                "name": todo['Наименование'],
                "start_date":  todo['ДатаНачала'],
                "deadline": todo['СрокВыполнения'],
                "is_completed": todo['Выполнено'],
                "actual_date": todo['ДатаФактическогоВыполнения'],
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
            # Проходим по списку договоров
            for project in projects_dict:
                contract = project['НомерДокумента']
                todoes = project['СписокРаботПоПроекту']
                resp = project['Ответственный']
                resp_rp = project['ОтветственныйРП']
                if contract in records:
                    cursor.execute('SELECT id FROM projectsapp_contracts where contract_number=%s', (contract, ))
                    id = cursor.fetchone()[0]
                    for todo in todoes:
                        fixture.append(self.get_dict(id, contract, todo, resp, resp_rp))

        return fixture
    
    def save(self):
        fixture=self.get_fixture()
        # Сохранение фикстуры
        with open(f'{self.import_path}{self.import_file}', mode='w+', encoding='utf-8') as file:
            json.dump(fixture, file, ensure_ascii=False, indent=4)

    def update_db(self):
        print(os.name)
	# Загрузка полученной фикстуры в приложение
        if os.name == 'nt':
            os.system('python -Xutf8 ./backend/indsol_web/manage.py loaddata projects.json --settings=indsol_web.settings.debug')
        else:
	        os.system(f'python -Xutf8 {self.worker_dir}/manage.py loaddata projects.json --settings=indsol_web.settings.pre_production')



if __name__ == "__main__":
    projects =  LoadProjects()
    # Настройки БД
    projects.dbname='indsol_test'
    projects.user='postgres'
    projects.password='123'
    projects.host='localhost'
    # Настройка файлов
    # Файл выгрузки
    projects.export_path = './backend/indsol_web/projectsapp/data/'
    projects.export_file= '111.json'
    # Файл фикстуры
    projects.import_path='./backend/indsol_web/projectsapp/fixtures/'
    projects.import_file='projects.json'

    projects.save()
    projects.update_db()
