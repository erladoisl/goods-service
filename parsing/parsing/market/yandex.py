import logging
from pyquery import PyQuery

try:
    from parsing.parsing.market.util import to_int, save_file
except:
    try:
        from util import to_int, save_file
    except:
        from market.util import to_int, save_file


def parse(html):
    '''
        Возвращает стоимость товара из HTML

        >>> parse('<div class="_3NaXx _3k4zY yCb5m" data-tid="ca3255c7"><span data-autotest-value="39" data-autotest-currency="₽"><span>39 990</span>&nbsp;<span class="-B-PA">₽</span></span></div><div class="_3NaXx _3kWlK" data-tid="ca3255c7"><span data-autotest-value="39" data-autotest-currency="₽"><span>39 990</span>&nbsp;<span class="-B-PA">₽</span></span></div><div class="_3NaXx _3PwoB ffKan" data-tid="ca3255c7"><span data-autotest-value="44" data-autotest-currency="₽"><span>44 990</span>&nbsp;<span class="-B-PA">₽</span></span></div>')
        39990
    '''
    price = -1
    pq = PyQuery(html)

    try:
        price = min([to_int(el) for el in pq(
            "div._3NaXx span span").text().split('₽') if el.strip() != ''])
    except:
        file_name = save_file('wrond_html', 'html', html)
        logging.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        return price


if __name__ == '__main__':
    with open('test/yandex.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
