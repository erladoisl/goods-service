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

        >>> parse('<div class="product-buy product-buy_one-line product-card-tabs__product-buy"><div class="product-buy__price-wrap product-buy__price-wrap_interactive"><div class="product-buy__price product-buy__price_active">43 699 ₽<span class="product-buy__prev">50 799</span></div><div class="product-buy__hint"></div><div class="product-buy__sub">или 4 233 ₽/ мес.</div></div><button class="button-ui notify-btn button-ui_passive button-ui_blue" data-commerce-tartget="PRODUCT_NOTIFY" data-gtm-vis-first-on-screen-32166084_1316="8783">Уведомить</button></div>')
        43699
        >>> parse('<div class="product-buy product-buy_one-line"><div class="product-buy__price-wrap"><div class="product-buy__price">999 ₽</div><div class="product-buy__hint"></div></div><button class="button-ui button-ui_white button-ui_icon wishlist-btn"></button><button class="button-ui buy-btn button-ui_brand button-ui_passive">Купить</button></div>')
        999
        >>> parse('<div class="product-buy product-buy_one-line"><div class="product-buy__price-wrap"><div class="product-buy__price">10 799 ₽</div><div class="product-buy__hint"></div><div class="product-buy__sub">Требуется предоплата</div></div><button class="button-ui button-ui_white button-ui_icon wishlist-btn"></button><button class="button-ui buy-btn button-ui_passive button-ui_brand">Купить</button></div>')
        10799
    '''
    price = -1
    pq = PyQuery(html)

    try:
        price = to_int(pq("div.product-buy__price").html().split('<span')[0])
    except:
        file_name = save_file('wrond_html', 'html', html)
        logging.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        return price


if __name__ == '__main__':
    with open('test/dns.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
