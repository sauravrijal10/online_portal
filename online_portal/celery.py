# from celery import Celery
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_portal.settings')


# app = Celery('online_portal', broker = 'redis://redis:6379/0')
# app.conf.broker_connection_retry_on_startup = True

# app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks()