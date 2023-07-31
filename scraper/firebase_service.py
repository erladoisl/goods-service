# module updates goods price. Appeals to firebase of goods-gazer project, gets products to update price by
# parsing html pages from different marketplaces. To see all supported sites go to modules\market.
# run update_prices to start

import asyncio
from datetime import datetime
from typing import Dict, List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from scraper.parsing import get_price
from config import firebase_admin_sdk_path, project_path
from aiohttp import ClientSession, ClientResponseError
import logging
import traceback
import config as c
import time

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('firebase_service')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])

cred = credentials.Certificate(firebase_admin_sdk_path)

firebase_admin.initialize_app(cred)
db = firestore.client()


def get_last_price(link, prices) -> Dict[str, str]:
    '''
        gets good's last fixed price by good's link from all prices
    '''
    link_prices = prices.where('link_id', '==', link.id)
    ordered_prices = link_prices.order_by(
        "date", direction=firestore.Query.DESCENDING)
    last_prices = ordered_prices.limit(1).stream()
    last_price_list = [price.to_dict() for price in last_prices]

    return last_price_list[0] if len(list(last_price_list)) > 0 else {}


def need_to_get_current_price(link, prices) -> bool:
    now = datetime.now()
    last_price = get_last_price(link, prices)
    date = last_price.get('date', None)

    return date == None or not (date.year == now.year and date.month == now.month and date.day == now.day)


def get_link_to_parse() -> Dict[str, str]:
    '''
        Возвращает ссылку на следующий товар, который находится в статусе active,
        и по которому нужно получить цену
    '''
    active_links = db.collection('links').where(
        'status', '==', 'active').stream()
    prices = db.collection('prices')

    for link in active_links:
        if need_to_get_current_price(link, prices):
            return {**(link.to_dict()), 'id': link.id}


def get_links_to_parse() -> List[Dict[str, str]]:
    '''
        Возвращает ссылки тех товаров, которые находятся в статусе active,
        и по которым нужно получить цену
    '''
    links = db.collection('links')
    active_links = links.where('status', '==', 'active').stream()
    prices = db.collection('prices')

    return [{**(link.to_dict()), 'id': link.id} for link in active_links if need_to_get_current_price(link, prices)]


def add_price(good_id: str, link_id: str, price: float) -> None:
    '''
        Добавляет текущую стоимость продукта по ссылке
    '''
    db.collection('prices')\
        .add({'good_id': good_id,
              'link_id': link_id,
              'price': price,
              'date': firestore.SERVER_TIMESTAMP})


def update_prices():
    '''
        Check's goods for necessity and get's all links to save actual prices
    '''
    links = get_links_to_parse()

    if len(links) == 0:
        log.info('Все продукты содержат актуальные данные')

    for link in links:
        log.info(f'Updating {link}')
        
        try:
            add_price(link['good_id'], link['id'], get_price(link['url']))
        except:
            log.error(
                f'Unable to get price in link {link["url"]}\n{traceback.format_exc()}')


async def update_price_async():
    '''
        Async check's goods for necessity and get's all links to save actual prices
    '''
    links = get_links_to_parse()

    if len(links) == 0:
        log.info('Все продукты содержат актуальные данные')

    tasks = []

    async with ClientSession() as session:
        for link in links:
            log.info(f'Получение актуальной цены по ссылке {link["url"]}')
            try:
                task = asyncio.ensure_future(fetch_url_data(session, url))
                tasks.append(task)
            except:
                log.error(
                    f'Unable to get price in link {link["url"]}\n{traceback.format_exc()}')

        await asyncio.gather(*tasks)


async def update_goods_price(good_id, id, url):
    log.debug(f"Updating goods {good_id} price by link: {url}")
    price = get_price(url)
    add_price(good_id, id, price)
    log.debug(f"Updating goods {good_id} price finished: {price}")


def set_ids(collection_name):
    objects = db.collection(collection_name).stream()

    for i, price in enumerate(objects):
        db.collection(collection_name).document(
            price.id).set({u'id': price.id}, merge=True)
