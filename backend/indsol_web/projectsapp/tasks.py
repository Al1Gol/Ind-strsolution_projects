from celery import shared_task
from time import sleep

@shared_task
def my_task():
    print('start my_tusk()')
    sleep(3)
    print('end my_tusk()')
    return 'my_tusk is comlited'
