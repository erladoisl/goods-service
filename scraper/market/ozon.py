import os
import traceback
from pyquery import PyQuery
from scraper.market.util import to_int, save_file
import logging
import config as c

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
    pq = PyQuery(html)
    
    try:
        price = to_int(pq('div[data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1]"] span span')[-1].text.split('₽')[0])
    except:
        file_name = save_file('wrond_ozon_html', 'html', html)
        log.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}\n {traceback.format_exc()}')
    finally:
        
        log.debug(f'Price: {price}')
        
        return price


if __name__ == '__main__':
    with open('C:/Users/User/Documents/goods_full/goods-service/modules/market/test/ozon.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
