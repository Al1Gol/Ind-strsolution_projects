import json
import psycopg2

conn = psycopg2.connect(dbname='indsol_test', user='postgres', 
                        password='123', host='localhost')
cursor = conn.cursor()

cursor.execute('SELECT contract_number FROM authapp_contracts')
records = cursor.fetchall()[0]

# Переменная для записи в фикстуру
fixture = []


def get_dict(project, num):
    dict_test = {
        "model": "projectsapp.projects",
        "pk": num,
        "fields": {
            "contract_id": None,
            "name": None,
            "start_date":  None,
            "deadline": None,
            "is_completed": None,
            "actual_date": None,
            "responsible": None,
            "responsible_rp": None
        }
    }
    return dict_test


# Исходный файл состоит из списка словарей
with open('./backend/indsol_web/projectsapp/data/111.json', mode='r', encoding='utf-8-sig') as file:
    projects_dict = json.loads(file.read())

    # Проходим по списку договоров
    for project in projects_dict:
        if project['НомерДокумента'] in records:
            fixture.append(get_dict(project, 1))
            print(project)
            print('-' * 10)
            print(project['НомерДокумента'])


with open('./backend/indsol_web/projectsapp/fixtures/projects.json', mode='w+', encoding='utf-8') as file:
    file.write(str(fixture))
print(records)