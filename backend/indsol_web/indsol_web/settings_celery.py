import os
from indsol_web.settings import pre_production
from django.core.management import call_command
from django.conf import settings
from celery import Celery
from celery import shared_task
from projectsapp.parsers import LoadProjects, LoadAdjustes

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indsol_web.settings.pre_production')

app = Celery('indsol_web')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def parser_projects_task(self):
    print('from settings_celery.py')
    projects =  LoadProjects()
    #Базовая директория
    projects.worker_dir=settings.BASE_DIR
    # Настройки БД
    projects.dbname=pre_production.DATABASES['default']['NAME']
    projects.user=pre_production.DATABASES['default']['USER']
    projects.password=pre_production.DATABASES['default']['PASSWORD']
    projects.host=pre_production.DATABASES['default']['HOST']
    # Путь файлов выгрузки
    projects.export_path = '/app/media/parse_data/'
    # Путь файлов фикстур
    projects.import_path=f'{settings.BASE_DIR}/projectsapp/fixtures/'
    # Файлы   
    projects.files = ['st_projects.json', 'export_projects.json']

    projects.load()

@app.task(bind=True, ignore_result=True)
def parser_adjust_task(self):
    print('from settings_celery.py')
    adjustes =  LoadAdjustes()
    #Базовая директория
    adjustes.worker_dir=settings.BASE_DIR
    # Настройки БД
    adjustes.dbname=pre_production.DATABASES['default']['NAME']
    adjustes.user=pre_production.DATABASES['default']['USER']
    adjustes.password=pre_production.DATABASES['default']['PASSWORD']
    adjustes.host=pre_production.DATABASES['default']['HOST']
    # Настройка файлов
    # Путь выгрузки
    adjustes.export_path = '/app/media/parse_data/'
    # Путь фикстуры
    adjustes.import_path=f'{settings.BASE_DIR}/projectsapp/fixtures/'
    # Файлы
    adjustes.files = ['st_adjust.json', 'export_adjust.json']

    adjustes.load()


@app.task(bind=True, ignore_result=True)
def cleanup_unused_media_task():
    print("Начало очистки неиспользуемых файлов")
    call_command("cleanup_unused_media", "--noinput")
    print("Окончание очистки неиспользуемых файлов")
    return  "cleanup unused media files is completed"
    
