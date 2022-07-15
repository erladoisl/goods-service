import logging
import os
from pyquery import PyQuery

try:
    from market.util import to_int, save_file
except:
    from util import to_int, save_file


def parse(html):
    '''
        Возвращает стоимость товара из HTML

        >>> parse('<div _ngcontent-serverapp-c156="" class="price price--pdp-emphasized-personal-price ng-star-inserted"><span _ngcontent-serverapp-c156="" class="price__main-value"> 119&nbsp;999&nbsp;₽ </span><span _ngcontent-serverapp-c156="" class="price__sale-value ng-star-inserted"> 149&nbsp;999 </span><!----></div>')
        119999
    '''
    price = -1
    pq = PyQuery(html)

    try:
        price = to_int(pq("span.price__main-value").text())
    except:
        file_name = save_file('wrond_html', 'html', html)
        logging.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        return price


if __name__ == '__main__':
    with open('test/mvideo.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
