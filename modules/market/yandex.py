import logging
import os
from pyquery import PyQuery
import re

try:
    from modules.market.util import to_int, save_file
except:
    try:
        from util import to_int, save_file
    except:
        from market.util import to_int, save_file

def get_price_by_reg(html) -> float:
    '''
        >>> get_price_by_reg('<div class="_3NaXx _3kWlK" data-tid="ca3255c7"><span data-autotest-value="9" data-autotest-currency="₽"><span>9 990</span>&nbsp;<span class="-B-PA">₽</span></span><span data-autotest-value="9" data-autotest-currency="₽"><span>9 990</span>&nbsp;<span class="-B-PA">₽</span></span></div></div>')
        9990
        >>> get_price_by_reg('<div class="_3NaXx _3kWlK" data-tid="ca3255c7"><span ><span>12 предложений от 13 000 ₽</span>&nbsp;<span class="-B-PA">₽</span></span></div></div>')
        13000
    '''
    try:
        return to_int(re.search('[0-9]+ предложений от [0-9 ]+ ₽', html).group(0).split('от')[-1])
    except:
        pq = PyQuery(html)
        
        return to_int(pq('[data-autotest-value]').text().split('\xa0₽')[0])


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
        try:
            price = get_price_by_reg(html)
        except:
            file_name = save_file('wrond_yandex_html', 'html', html)
            logging.error(
                f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        return price


if __name__ == '__main__':
    with open('test/mvideo.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
