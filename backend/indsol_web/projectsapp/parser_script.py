import json
import psycopg2
import os

def get_dict(id, contract, todo):
    dict_test = {
        "model": "projectsapp.projects",
        #"pk": id,
        "fields": {
            "contract_id": contract,
            "name": todo['Наименование'],
            "start_date":  todo['ДатаНачала'],
            "deadline": todo['СрокВыполнения'],
            "is_completed": todo['Выполнено'],
            "actual_date": todo['ДатаФактическогоВыполнения'],
            "responsible": None,
            "responsible_rp": None
        }
    }
    return dict_test

def unpack(projects):
    return projects[0]

conn = psycopg2.connect(dbname='indsol_test', user='postgres', 
                        password='123', host='localhost')
cursor = conn.cursor()

cursor.execute('SELECT contract_number FROM projectsapp_contracts')
records = [el[0] for el in cursor.fetchall()]

# Переменная для записи в фикстуру
fixture = []

# Исходный файл состоит из списка словарей
with open('./backend/indsol_web/projectsapp/data/111.json', mode='r', encoding='utf-8-sig') as file:
    projects_dict = json.loads(file.read())

    # Проходим по списку договоров
    for id, project in enumerate(projects_dict):
        contract = project['НомерДокумента']
        todoes = project['СписокРаботПоПроекту']
        if contract in records:
            for todo in todoes:
                fixture.append(get_dict(id, contract, todo))

# Сохранение фикстуры
with open('./backend/indsol_web/projectsapp/fixtures/projects.json', mode='w+', encoding='utf-8') as file:
    json.dump(fixture, file, ensure_ascii=False, indent=4)

# Загрузка полученной фикстуры в приложение
os.system('python -Xutf8 ./backend/indsol_web/manage.py loaddata projects.json --settings=indsol_web.settings.debug')