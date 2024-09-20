from django.core.management import call_command

from celery import shared_task

@shared_task
def cleanup_unused_media_task():
    print("Start cleanup unused media files")
    call_command("cleanup_unused_media", "--noinput")
    print("End cleanup unused media files")
    return  "cleanup unused media files is completed"