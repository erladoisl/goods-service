import os
from pyquery import PyQuery
from scraper.market.util import to_int, save_file
import logging
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('scraper.market.yandex')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])


def parse(html: str) -> int:
    price = -1

    try:
        if for_sale(html):
            pq = PyQuery(html)

            if len(pq('span[data-auto="morePrices"]')) > 0:
                price = to_int(pq('span[data-auto="morePrices"]')[0].getchildren()[-1].text)
            elif len(pq('meta[itemprop="price"]')) > 0:
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
    res = 'Нет в продаже' not in html

    if not res:
        log.info('Товар закончился в yandex')

    return res

if __name__ == '__main__':
    with open('test/mvideo.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
