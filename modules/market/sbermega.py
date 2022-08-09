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

        >>> parse('<div class="prod-buy"><div class="pdp-price-history__lowest-price">20 900&nbsp;₽</div><div class="pdp-sales-block pdp-first-screen__sales-block pdp-sales-block_active"><div class="pdp-sales-block__top"><div class="pdp-sales-block__circle"><svg class="pdp-sales-block__circle-checked svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-check"></use></svg></div><div class="pdp-sales-block__title">Доставка завтра или позже</div></div><!----><div class="pdp-sales-block__price"><div class="pdp-sales-block__price-wrap pdp-sales-block__price-wrap_active"><!----><span class="pdp-sales-block__price-final">21 990 ₽<meta itemprop="price" content="21990"><meta itemprop="priceCurrency" content="RUB"><link itemprop="availability" href="http://schema.org/InStock" content="InStock"><link itemprop="url" content="https://sbermegamarket.ru/"></span><div itemscope="itemscope" itemprop="offers" itemtype="http://schema.org/AggregateOffer"><meta itemprop="offerCount" content="4"><meta itemprop="highPrice" content="22999"><meta itemprop="lowPrice" content="20900"><meta itemprop="priceCurrency" content="RUB"></div></div><div class="money-bonus pdp-sales-block__bonus lg pdp-sales-block__bonus_active"><span class="bonus-percent"><span>8%</span></span> <span class="bonus-amount"><span>1 760</span></span> <svg class="svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-coins"></use></svg></div></div><!----><!----><!----><div class="pdp-sales-block__delivery"><div class="pdp-sales-block__delivery-type">Курьером продавца — 350 ₽<!----></div><div class="pdp-sales-block__delivery-date">с 4 по 5 августа</div></div><!----><!----><!----><div class="pdp-sales-block__button"><div class="experiment-wrapper catalog-buy-button catalog-buy-button_default catalog-buy-button_orientation-vertical catalog-buy-button_width-full catalog-buy-button_exp-88857-2"><button type="button" class="catalog-buy-button__button btn sm">Купить</button></div></div><div class="pdp-sales-block__merchant"><span>Продавец: <a href="/shop/qukeru/" class="pdp-offer-block__merchant-link">Quke.ru</a><svg class="legal-info-hint pdp-offer-block__merchant-hint sm svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-info"></use></svg></span></div></div><div class="pdp-sales-block pdp-first-screen__sales-block"><div class="pdp-sales-block__top"><div class="pdp-sales-block__circle"><svg class="pdp-sales-block__circle-checked svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-check"></use></svg></div><div class="pdp-sales-block__title">Забрать сегодня в магазине</div></div><!----><div class="pdp-sales-block__price"><div class="pdp-sales-block__price-wrap"><span class="pdp-sales-block__price-prefix">от</span><span class="pdp-sales-block__price-final">20 900 ₽<meta itemprop="price" content="20900"><meta itemprop="priceCurrency" content="RUB"><link itemprop="availability" href="http://schema.org/InStock" content="InStock"><link itemprop="url" content="https://sbermegamarket.ru/"></span><div itemscope="itemscope" itemprop="offers" itemtype="http://schema.org/AggregateOffer"><meta itemprop="offerCount" content="4"><meta itemprop="highPrice" content="22999"><meta itemprop="lowPrice" content="20900"><meta itemprop="priceCurrency" content="RUB"></div></div><div class="money-bonus pdp-sales-block__bonus lg"><span class="bonus-percent"><span>8%</span></span> <span class="bonus-amount"><span>1 672</span></span> <svg class="svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-coins"></use></svg></div></div><!----><!----></div><div class="pdp-first-screen__more-offers-button-wrapper"><a href="/catalog/details/smartfon-poco-m4-pro-256gb-power-black-100030991337/#?details_block=prices" class="pdp-first-screen__more-offers-button pdp-first-screen__more-offers-button_bordered">Еще 2 предложения от 22 990 ₽</a></div><!----><!----></div>')
        20900
    '''
    price = -1
    pq = PyQuery(html)

    try:
        price = to_int(pq("div.pdp-price-history__lowest-price").text())
    except:
        file_name = save_file('wrond_sbermega_html', 'html', html)
        logging.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}')
    finally:
        return price


if __name__ == '__main__':
    with open('modules/market/test/sbermega.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))

    