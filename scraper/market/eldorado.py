from pyquery import PyQuery
from scraper.market.util import to_int, save_file
import logging
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('scraper.market.eldorado')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])


def parse(html):
    '''
        Возвращает стоимость товара из HTML
    '''
    price = -1

    try:
        if for_sale(html):
            pq = PyQuery(html)
            price = to_int(pq(".catalogItemDetail .i-flocktory").attr['data-fl-item-price'])
    except:
        file_name = save_file('eldorado_html', 'html', html)
        log.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        
        log.debug(f'Price: {price}')
        
        return price



def for_sale(html):
    '''
        Возвращает True если товар все еще продается. Иначе - False
    '''
    res = 'Последняя цена:' not in html

    if not res:
        log.info('Товар закончился в eldorado')

    return res


if __name__ == '__main__':
    with open('test/eldorado.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))

    