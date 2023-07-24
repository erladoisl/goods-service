import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goods_service.settings')

app = Celery('goods_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'sent_spam_every_one_minutes': {
        'task': 'scraper.tasks.test_every_min',
        'schedule': crontab(minute='*/1')
    },
    'update_prices': {
        'task': 'scraper.tasks.update_prices_task',
        'schedule': crontab(minute='*/1')
    },
    
}
