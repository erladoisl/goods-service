from celery import shared_task
from goods_service.celery import app
from scraper.firebase_service import update_prices
import logging
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('sraper.task')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])


@app.task
def test_every_min():
    log.info('test_every_min')
    
    return True

@app.task
def update_prices_task():
    log.debug('update_prices_task')
    update_prices()
    
    return True


@app.task
def update_goods_price_task(good_id, id, url):
    log.debug('update_goods_price_task')
    update_prices()
    
    return True

