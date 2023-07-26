import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goods_service.settings')

app = Celery('goods_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update_prices': {
        'task': 'scraper.tasks.update_prices_task',
        'schedule': crontab(minute='*/1')
    },
    
}
