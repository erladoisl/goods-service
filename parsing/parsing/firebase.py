from datetime import datetime
from typing import Dict, List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import traceback
from config import project_path
try:
    from parsing import get_price
except:
    from parsing.parsing.parsing import get_price

cred = credentials.Certificate(f'{project_path}parsing/parsing/goods-gazer-firebase-adminsdk.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

def get_last_price(link, prices) -> Dict[str, str]:
    link_prices = prices.where('link_id', '==', link.id)
    ordered_prices = link_prices.order_by("date", direction=firestore.Query.DESCENDING)
    last_prices = ordered_prices.limit(1).stream()
    last_price_list = [price.to_dict() for price in last_prices]
    
    return last_price_list[0] if len(list(last_price_list)) > 0 else {}


def need_to_get_current_price(link, prices) -> bool:
    now = datetime.now()
    last_price = get_last_price(link, prices)
    date = last_price.get('date', None)

    return date == None or not (date.year == now.year and date.month == now.month and date.day == now.day)


def get_links_to_parse() -> List[Dict[str,str]]:
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
    db_good = db.collection('prices')\
        .add({'good_id': good_id, 
              'link_id': link_id, 
              'price': price,
              'date': firestore.SERVER_TIMESTAMP})


def update_prices():
    '''
        Обновляет текущую цену для всех активных ссылок
    '''
    links = get_links_to_parse()

    if len(links) == 0:
        logging.info('Все продукты содержат актуальные данные')

    for link in links:
        logging.info(f'Получение актуальной цены по ссылке {link["url"]}')
        try:
            add_price(link['good_id'], link['id'], get_price(link['url']))
        except:
            logging.error(f'Unable to get price in link {link["url"]}\n{traceback.format_exc()}')
