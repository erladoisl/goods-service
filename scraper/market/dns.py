from pyquery import PyQuery
from scraper.market.util import to_int, save_file
import logging
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('scraper.market.dns')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])

def parse(html):
    '''
        Возвращает стоимость товара из HTML
    '''
    price = -1
    pq = PyQuery(html)

    try:
        price = to_int(pq("div.product-buy__price").html().split('<span')[0])
    except:
        file_name = save_file('dns_html', 'html', html)
        log.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        
        log.debug(f'Price: {price}')
        
        return price


if __name__ == '__main__':
    with open('test/dns.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
