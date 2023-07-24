import os
import traceback
from pyquery import PyQuery
from scraper.market.util import to_int, save_file
import logging
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('scraper.market.ozon')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])


def parse(html):
    '''
        Возвращает стоимость товара из HTML

        >>> parse('<<div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1]"><div class="z5m" data-widget="webPrice"><!----> <div slot="content" class="m6z zm6"><!----> <div class="zm3 m5z z6m"><div><span class="m4z"><span>12 490 ₽</span>&nbsp;</span></div></div> <!----> <!----></div> <!----></div></div>')
        12490
        >>> parse('<div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1]"><div class="z5m" data-widget="webPrice"><!----> <div slot="content" class="m6z zm6"><!----> <div class="zm3 m5z z6m"><div><span class="m4z zm4"><span>29 994 ₽</span>&nbsp;</span><span class="mz5">34 493 ₽</span></div></div> <!----> <!----></div> <!----></div></div>')
        29994
        >>> parse('<div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1]"><div class="z5m" data-widget="webPrice"><!----> <div slot="content" class="m6z mz8"><div class="z1m z7m"><span class="mz2 zm2">1&nbsp;847&nbsp;₽</span><span class="mz3">× 6 мес<div class="ui-k1 vk m3z"><div class="ui-f2"><button tabindex="0" type="button" class="ui-f4" style="border-radius:8px;"><span class="ui-f6 ui-g7 ui-j0" style="border-radius:8px;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="ui-i9" style="color: var(--ozBGQuaternary);"><path fill="currentColor" d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16ZM8 5a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1 3v4a1 1 0 1 1-2 0V8a1 1 0 0 1 2 0Z"></path></svg><span class="ui-j3"></span></span></button></div> </div></span></div> <div class="zm3 m5z z6m"><div><span class="m4z zm4"><span>9 593 ₽</span>&nbsp;</span><span class="mz5">12 362 ₽</span></div></div> <!----> <div class="m7z"><div data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1][0][0]"><div class="ui-b7a ui-ba8 ui-b8a mx5" style="background-color: var(--ozCtrlPositive); color: var(--ozWhite);" data-widget="webOzonAccountPrice"><div class="ui-a9b">8 778 ₽  при оплате Ozon Картой</div><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="ui-ba9 ui-b9a ui-ac" style="color: var(--ozWhite);"><path fill="currentColor" d="M8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12Zm0-8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1 2v3a1 1 0 1 1-2 0V8a1 1 0 0 1 2 0Z"></path></svg></div></div></div></div> <!----></div></div>')
        9593
    '''
    price = -1
    pq = PyQuery(html)
    
    try:
        price = to_int(pq('div[data-replace-layout-path="[4][0][2][0][1][0][1][0][0][1]"] span span')[-1].text.split('₽')[0])
    except:
        file_name = save_file('wrond_ozon_html', 'html', html)
        log.error(
            f'Ошибка получения стоимости товара, текст HTML будет сохранен в файл: {file_name}\n {traceback.format_exc()}')
    finally:
        
        log.debug(f'Price: {price}')
        
        return price


if __name__ == '__main__':
    with open('C:/Users/User/Documents/goods_full/goods-service/modules/market/test/ozon.html', 'r', encoding="utf-8") as f:
        html = ''.join(f.readlines())

        print(parse(html))
