from scraper.selenium_request import Request

from scraper.market.dns import parse as dns_parse
from scraper.market.eldorado import parse as eldorado_parse
from scraper.market.yandex import parse as yandex_parse
from scraper.market.mvideo import parse as mvideo_parse
from scraper.market.sbermega import parse as sbermega_parse
from scraper.market.ozon import parse as ozon_parse

from config import project_path, chromedriver_path

import logging
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('parsing')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])

parser = {
    'www.dns-shop.ru': dns_parse,
    'www.eldorado.ru': eldorado_parse,
    'market.yandex.ru': yandex_parse,
    'www.mvideo.ru': mvideo_parse,
    'sbermegamarket': sbermega_parse,
    'www.ozon.ru': ozon_parse,
}


def get_html(url: str, domain: str, class_name: str) -> str:
    '''
        1. Возращает содержимое html страницы по ссылке на неё
        2. Добавляет для домена в links_history текущее время как последнее время обращения

        >>> get_html(f'http://x.com/', 'x.com')
        '<html><head></head><body>x</body></html>'
    '''
    
    request = Request(url, domain)
    text = request.get_selenium_res(class_name)

    log.info('HTML page successfully loaded!')

    return text


def get_domain(link):
    '''
        Возвращает домен

        >>> get_domain('https://market.yandex.ru/product--umnaia-kolonka-yandex-stantsiia-2-s-golosovym-pomoshchnikom-alisa-komplekt-ustroistv-aqara-s-umnoi-lampochkoi/1753411994?sku=101757104728&cpa=1&nid=26992350')
        'market.yandex.ru'
        >>> get_domain('https://www.dns-shop.ru/product/82fca53498c53332/vstraivaemaa-posudomoecnaa-masina-electrolux-edm43210l/')
        'www.dns-shop.ru'
        >>> get_domain('https://www.mvideo.ru/products/smartfon-apple-iphone-13-pro-max-128gb-alpine-green-30063190')
        'www.mvideo.ru'
        >>> get_domain('https://www.ozon.ru/product/smesitel-qri-dizaynerskiy-iz-latuni-dlya-rakoviny-kollektsii-io-666954132/?advert=qp34iejOwy1z_RXeDMCzKfZbKVQI5V46pnXtR3fhuZ_OP85ixNjTsCejAFrLKPHTZyiVg8AA924nxCfWbrZnyQSLhKxKgWenc9qrPvmbozy3si2C3W73FmSEq_ddLJ2a4WrWrWo10KHbgRRkt60DwXDRcpX45BwTfeWFSFMq7vowNsixzLMoITzDzg&hs=1&sh=rauJU2tnJQ')
        'www.ozon.ru'
    '''
    splited = list(link.split('/'))

    return splited[2] if len(splited) > 2 else None


def get_price(link):
    ''' 
        На основе ссылки на карточку товара в интернет магазине возвращает текущую стоимость

        >>> price = get_price('https://market.yandex.ru/product--vstraivaemaia-posudomoechnaia-mashina-weissgauff-bdw-4533-d/775151031')
        >>> price
        39990
        >>> price = get_price('https://www.dns-shop.ru/product/19e316eba3252eb1/vstraivaemaa-posudomoecnaa-masina-dexp-dw-b45n6avlg/')
        >>> price
        15099
        >>> price = get_price('https://www.eldorado.ru/cat/detail/smartfon-xiaomi-redmi-9c-nfc-2-32gb-midnight-gray/')
        >>> price
        9999
    '''
    domain = get_domain(link)
    log.info(f'Domain: {domain}')
    html = get_html(link, domain, c.CLASS_NAME.get(domain, ''))

    return parser[domain](html)


if __name__ == '__main__':
    from market.util import save_file

    link = 'https://www.eldorado.ru/cat/detail/smartfon-redmi-9a-32gb-granite-gray/'
    html = get_html(link, '')
    save_file('eldo42', 'html', html)
