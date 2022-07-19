from datetime import datetime
from typing import Dict, List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
try:
    from parsing import get_price
except:
    from parsing.parsing.parsing import get_price

cred = credentials.Certificate('parsing/parsing/goods-gazer-firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_last_price(link, prices) -> Dict[str, str]:
    link_prices = prices.where('link_id', '==', link.id)
    ordered_prices = link_prices.order_by("date", direction=firestore.Query.DESCENDING)
    last_prices = ordered_prices.limit(1)
    last_price = [price.to_dict() for price in last_prices.stream()][0]
    
    return last_price


def need_to_get_current_price(link, prices) -> bool:
    now = datetime.now()
    last_price = get_last_price(link, prices)
    date = last_price['date']

    return not (date.year == now.year and date.month == now.month and date.day == now.day)


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
        print('Все продукты содержат актуальные данные')

    for link in links:
        print(f'Получение актуальной цены по ссылке {link["url"]}')
        add_price(link['good_id'], link['id'], get_price(link['url']))
