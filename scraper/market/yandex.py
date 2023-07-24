import os
import re
from pyquery import PyQuery
from scraper.market.util import to_int, save_file
import logging
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('scraper.market.yandex')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])


def get_price_by_reg(html) -> float:
    try:
        return to_int(re.search('[0-9]+ предложений от [0-9 ]+ ₽', html).group(0).split('от')[-1]) 
    except:
        pq = PyQuery(html)
        
        return to_int(pq('[data-autotest-value]').text().split('\xa0₽')[0])


def parse(html):
    price = -1
    pq = PyQuery(html)

    try:
        price = to_int(pq("span.price__main-value").text())
    except:
        try:
            price = get_price_by_reg(html)
        except:
            file_name = save_file('wrond_yandex_html', 'html', html)
            log.error(
                f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        log.debug(f'Price: {price}')
        
        return price


if __name__ == '__main__':
    with open('test/mvideo.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
