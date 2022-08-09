import logging
from pyquery import PyQuery

try:
    from modules.market.util import to_int, save_file
except:
    try:
        from util import to_int, save_file
    except:
        from market.util import to_int, save_file


def parse(html):
    '''
        Возвращает стоимость товара из HTML

        >>> parse('<div class="product-box-price__active">16&nbsp;999&nbsp;р.</div><div class="product-box-price__active">16&nbsp;999&nbsp;р.</div><div class="product-box-price__active">16&nbsp;999&nbsp;р.</div>')
        16999
    '''
    price = -1
    pq = PyQuery(html)

    try:
        price = to_int(pq("div.product-box-price__active").text().split('р.')[0])
    except:
        file_name = save_file('wrond_eldorado_html', 'html', html)
        logging.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        return price


if __name__ == '__main__':
    with open('test/eldorado.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))

    