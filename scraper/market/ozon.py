import os
import traceback
from pyquery import PyQuery
from scraper.market.util import to_int, save_file
import logging
import config as c
import re

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('scraper.market.ozon')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])


def parse(html):
    '''
        Возвращает стоимость товара из HTML
    '''
    price = -1

    try:
        if for_sale(html):
            res = re.search('<span class="sk0">([0-9]+\u2009){0,}₽', html)
            log.debug(f're result: {res}')

            if res:
                price = int(
                    re.search('(\d+\u2009){0,}(?=₽)', res[0])[0].replace('\u2009', ''))
    except:
        file_name = save_file('ozon_html', 'html', html)
        log.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}\n {traceback.format_exc()}')
    finally:

        log.debug(f'Price: {price}')

        return price


def for_sale(html):
    '''
        Возвращает True если товар все еще продается. Иначе - False
    '''
    res = 'Этот товар закончился' not in html

    if not res:
        log.info('Товар закончился в ozon')

    return res


if __name__ == '__main__':
    with open('C:/Users/User/Documents/goods_full/goods-service/modules/market/test/ozon.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
