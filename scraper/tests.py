from django.test import TestCase
import scraper.market.dns as dns
import scraper.market.eldorado as eldorado
import scraper.market.mvideo as mvideo
import scraper.market.ozon as ozon
import scraper.market.yandex as yandex
import scraper.market.sbermega as sbermega


class DNSTestCase(TestCase):
    def test_parse_success(self):
        result1 = dns.parse('<div class="product-buy product-buy_one-line product-card-tabs__product-buy"><div class="product-buy__price-wrap product-buy__price-wrap_interactive"><div class="product-buy__price product-buy__price_active">43 699 ₽<span class="product-buy__prev">50 799</span></div><div class="product-buy__hint"></div><div class="product-buy__sub">или 4 233 ₽/ мес.</div></div><button class="button-ui notify-btn button-ui_passive button-ui_blue" data-commerce-tartget="PRODUCT_NOTIFY" data-gtm-vis-first-on-screen-32166084_1316="8783">Уведомить</button></div>')
        self.assertEqual(result1, 43699)
        
        result2 = dns.parse('<div class="product-buy product-buy_one-line"><div class="product-buy__price-wrap"><div class="product-buy__price">999 ₽</div><div class="product-buy__hint"></div></div><button class="button-ui button-ui_white button-ui_icon wishlist-btn"></button><button class="button-ui buy-btn button-ui_brand button-ui_passive">Купить</button></div>')
        self.assertEqual(result2, 999)
        
        result3 = dns.parse('<div class="product-buy product-buy_one-line"><div class="product-buy__price-wrap"><div class="product-buy__price">10 799 ₽</div><div class="product-buy__hint"></div><div class="product-buy__sub">Требуется предоплата</div></div><button class="button-ui button-ui_white button-ui_icon wishlist-btn"></button><button class="button-ui buy-btn button-ui_passive button-ui_brand">Купить</button></div>')
        self.assertEqual(result3, 10799)
        

class EldoradoTestCase(TestCase):
    def test_parse_success(self):
        result1 = eldorado.parse('<div class="product-box-price__active">16&nbsp;999&nbsp;р.</div><div class="product-box-price__active">16&nbsp;999&nbsp;р.</div><div class="product-box-price__active">16&nbsp;999&nbsp;р.</div>')
        self.assertEqual(result1, 16999)
        

class MvideoTestCase(TestCase):
    def test_parse_success(self):
        result1 = mvideo.parse('<div _ngcontent-serverapp-c156="" class="price price--pdp-emphasized-personal-price ng-star-inserted"><span _ngcontent-serverapp-c156="" class="price__main-value"> 119&nbsp;999&nbsp;₽ </span><span _ngcontent-serverapp-c156="" class="price__sale-value ng-star-inserted"> 149&nbsp;999 </span><!----></div>')
        self.assertEqual(result1, 119999)

class OzonTestCase(TestCase):
    def test_parse_success(self):
        result1 = ozon.parse('<<div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1]"><div class="z5m" data-widget="webPrice"><!----> <div slot="content" class="m6z zm6"><!----> <div class="zm3 m5z z6m"><div><span class="m4z"><span>12 490 ₽</span>&nbsp;</span></div></div> <!----> <!----></div> <!----></div></div>')
        self.assertEqual(result1, 12490)
        
        result2 = ozon.parse('<div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1]"><div class="z5m" data-widget="webPrice"><!----> <div slot="content" class="m6z zm6"><!----> <div class="zm3 m5z z6m"><div><span class="m4z zm4"><span>29 994 ₽</span>&nbsp;</span><span class="mz5">34 493 ₽</span></div></div> <!----> <!----></div> <!----></div></div>')
        self.assertEqual(result2, 29994)
        
        result3 = ozon.parse('<div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1]"><div class="z5m" data-widget="webPrice"><!----> <div slot="content" class="m6z mz8"><div class="z1m z7m"><span class="mz2 zm2">1&nbsp;847&nbsp;₽</span><span class="mz3">× 6 мес<div class="ui-k1 vk m3z"><div class="ui-f2"><button tabindex="0" type="button" class="ui-f4" style="border-radius:8px;"><span class="ui-f6 ui-g7 ui-j0" style="border-radius:8px;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="ui-i9" style="color: var(--ozBGQuaternary);"><path fill="currentColor" d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16ZM8 5a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1 3v4a1 1 0 1 1-2 0V8a1 1 0 0 1 2 0Z"></path></svg><span class="ui-j3"></span></span></button></div> </div></span></div> <div class="zm3 m5z z6m"><div><span class="m4z zm4"><span>9 593 ₽</span>&nbsp;</span><span class="mz5">12 362 ₽</span></div></div> <!----> <div class="m7z"><div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1][0][0]"><div class="ui-b7a ui-ba8 ui-b8a mx5" style="background-color: var(--ozCtrlPositive); color: var(--ozWhite);" data-widget="webOzonAccountPrice"><div class="ui-a9b">8 778 ₽  при оплате Ozon Картой</div><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="ui-ba9 ui-b9a ui-ac" style="color: var(--ozWhite);"><path fill="currentColor" d="M8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12Zm0-8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1 2v3a1 1 0 1 1-2 0V8a1 1 0 0 1 2 0Z"></path></svg></div></div></div></div> <!----></div></div>')
        self.assertEqual(result3, 9593)
        
        
class SbermegaTestCase(TestCase):
    def test_parse_success(self):
        result1 = sbermega.parse('<div class="prod-buy"><div class="pdp-price-history__lowest-price">20 900&nbsp;₽</div><div class="pdp-sales-block pdp-first-screen__sales-block pdp-sales-block_active"><div class="pdp-sales-block__top"><div class="pdp-sales-block__circle"><svg class="pdp-sales-block__circle-checked svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-check"></use></svg></div><div class="pdp-sales-block__title">Доставка завтра или позже</div></div><!----><div class="pdp-sales-block__price"><div class="pdp-sales-block__price-wrap pdp-sales-block__price-wrap_active"><!----><span class="pdp-sales-block__price-final">21 990 ₽<meta itemprop="price" content="21990"><meta itemprop="priceCurrency" content="RUB"><link itemprop="availability" href="http://schema.org/InStock" content="InStock"><link itemprop="url" content="https://sbermegamarket.ru/"></span><div itemscope="itemscope" itemprop="offers" itemtype="http://schema.org/AggregateOffer"><meta itemprop="offerCount" content="4"><meta itemprop="highPrice" content="22999"><meta itemprop="lowPrice" content="20900"><meta itemprop="priceCurrency" content="RUB"></div></div><div class="money-bonus pdp-sales-block__bonus lg pdp-sales-block__bonus_active"><span class="bonus-percent"><span>8%</span></span> <span class="bonus-amount"><span>1 760</span></span> <svg class="svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-coins"></use></svg></div></div><!----><!----><!----><div class="pdp-sales-block__delivery"><div class="pdp-sales-block__delivery-type">Курьером продавца — 350 ₽<!----></div><div class="pdp-sales-block__delivery-date">с 4 по 5 августа</div></div><!----><!----><!----><div class="pdp-sales-block__button"><div class="experiment-wrapper catalog-buy-button catalog-buy-button_default catalog-buy-button_orientation-vertical catalog-buy-button_width-full catalog-buy-button_exp-88857-2"><button type="button" class="catalog-buy-button__button btn sm">Купить</button></div></div><div class="pdp-sales-block__merchant"><span>Продавец: <a href="/shop/qukeru/" class="pdp-offer-block__merchant-link">Quke.ru</a><svg class="legal-info-hint pdp-offer-block__merchant-hint sm svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-info"></use></svg></span></div></div><div class="pdp-sales-block pdp-first-screen__sales-block"><div class="pdp-sales-block__top"><div class="pdp-sales-block__circle"><svg class="pdp-sales-block__circle-checked svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-check"></use></svg></div><div class="pdp-sales-block__title">Забрать сегодня в магазине</div></div><!----><div class="pdp-sales-block__price"><div class="pdp-sales-block__price-wrap"><span class="pdp-sales-block__price-prefix">от</span><span class="pdp-sales-block__price-final">20 900 ₽<meta itemprop="price" content="20900"><meta itemprop="priceCurrency" content="RUB"><link itemprop="availability" href="http://schema.org/InStock" content="InStock"><link itemprop="url" content="https://sbermegamarket.ru/"></span><div itemscope="itemscope" itemprop="offers" itemtype="http://schema.org/AggregateOffer"><meta itemprop="offerCount" content="4"><meta itemprop="highPrice" content="22999"><meta itemprop="lowPrice" content="20900"><meta itemprop="priceCurrency" content="RUB"></div></div><div class="money-bonus pdp-sales-block__bonus lg"><span class="bonus-percent"><span>8%</span></span> <span class="bonus-amount"><span>1 672</span></span> <svg class="svg-icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#i-coins"></use></svg></div></div><!----><!----></div><div class="pdp-first-screen__more-offers-button-wrapper"><a href="/catalog/details/smartfon-poco-m4-pro-256gb-power-black-100030991337/#?details_block=prices" class="pdp-first-screen__more-offers-button pdp-first-screen__more-offers-button_bordered">Еще 2 предложения от 22 990 ₽</a></div><!----><!----></div>')
        self.assertEqual(result1, 20900)
        
        
        
class YandexTestCase(TestCase):
    def test_get_price_by_reg_success(self):
        result1 = yandex.get_price_by_reg('<div class="_3NaXx _3kWlK" data-tid="ca3255c7"><span data-autotest-value="9" data-autotest-currency="₽"><span>9 990</span>&nbsp;<span class="-B-PA">₽</span></span><span data-autotest-value="9" data-autotest-currency="₽"><span>9 990</span>&nbsp;<span class="-B-PA">₽</span></span></div></div>')
        self.assertEqual(result1, 9990)
        
        result2 = yandex.get_price_by_reg('<div class="_3NaXx _3kWlK" data-tid="ca3255c7"><span ><span>12 предложений от 13 000 ₽</span>&nbsp;<span class="-B-PA">₽</span></span></div></div>')
        self.assertEqual(result2, 13000)
        
        
    def test_parse_success(self):
        result1 = yandex.parse('<div _ngcontent-serverapp-c156="" class="price price--pdp-emphasized-personal-price ng-star-inserted"><span _ngcontent-serverapp-c156="" class="price__main-value"> 119&nbsp;999&nbsp;₽ </span><span _ngcontent-serverapp-c156="" class="price__sale-value ng-star-inserted"> 149&nbsp;999 </span><!----></div>')
        self.assertEqual(result1, 119999)