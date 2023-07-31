from pyquery import PyQuery
from scraper.market.util import to_int, save_file
import logging
import traceback
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('scraper.market.yandex')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])


def parse(html: str) -> int:
    '''
        Парсит html страницу и возвращает самую меньшую цену за товар.
        Возвращает -1 - если товар не найден или не продается, или при какой-то ошибке(См. логи)
    '''
    price = -1

    try:
        if for_sale(html):
            pq = PyQuery(html)

            if len(pq('span[data-auto="morePrices"]')) > 0:
                price_in_str = pq('span[data-auto="morePrices"]')[0].getchildren()[-1].text
                
                if price_in_str:
                    price = to_int(pq('span[data-auto="morePrices"]')[0].getchildren()[-1].text)
                
            if price == -1:
                if len(pq('meta[itemprop="price"]')) > 0:
                    price = to_int(pq('meta[itemprop="price"]')[0].attrib['content'])
                else:
                    price = to_int(pq('span[data-auto="mainPrice"]')[0].getchildren()[0].text)
    except:
        file_name = save_file('yandex_html', 'html', html)
        log.error(f'Error while getting price {file_name}')
    finally:
        log.debug(f'Price: {price}')
        
        return price



def for_sale(html):
    '''
        Возвращает True если товар все еще продается. Иначе - False
    '''
    res = 'Нет в продаже' not in html and 'Код ошибки: 404' not in html

    if not res:
        log.info('Товар закончился в yandex')

    return res
