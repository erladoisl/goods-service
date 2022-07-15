from datetime import datetime
from time import sleep
from typing import Dict
from selenium import webdriver
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
# from .market.dns import parse as dns_parse
# from .market.eldorado import parse as eldorado_parse
# from .market.yandex import parse as yandex_parse

# parser = {
#     'www.dns-shop.ru': dns_parse,
#     'www.eldorado.ru': eldorado_parse,
#     'market.yandex.ru': yandex_parse
# }

links_history = {}

def get_timeout_for_domain(domain: str, link_history: Dict[str, datetime]) -> float:
    '''
        Возвращает время, через которое нужно обратиться по домену,
        учитывая то, что по одному домену нельзя обращаться чаще раз в 5 сек
    '''
    pass


def get_html(url: str, domain: str) -> str:
    '''
        1. Возращает содержимое html страницы по ссылке на неё
        2. Добавляет для домена в links_history текущее время как последнее время обращения

        >>> domain = 'x.com'
        >>> get_html(f'http://{domain}/', domain)
        'x'
        >>> links_history[domain].ctime() == datetime.now().ctime()
        True
        >>> domain = 'x.com'
        >>> get_html(f'https://www.mvideo.ru/products/smartfon-apple-iphone-13-pro-max-128gb-alpine-green-30063190', domain)
        'big data - that test fails'
    '''
    global links_history
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)

    html = driver.page_source
    sleep(5)
    text = html
    driver.close()
    links_history[domain] = datetime.now()

    return text
  

def get_domen(link):
    '''
        Возвращает домен

        >>> get_domen('https://market.yandex.ru/product--umnaia-kolonka-yandex-stantsiia-2-s-golosovym-pomoshchnikom-alisa-komplekt-ustroistv-aqara-s-umnoi-lampochkoi/1753411994?sku=101757104728&cpa=1&nid=26992350')
        'market.yandex.ru'
        >>> get_domen('https://www.dns-shop.ru/product/82fca53498c53332/vstraivaemaa-posudomoecnaa-masina-electrolux-edm43210l/')
        'www.dns-shop.ru'
        >>> get_domen('https://www.mvideo.ru/products/smartfon-apple-iphone-13-pro-max-128gb-alpine-green-30063190')
        'www.mvideo.ru'
    '''
    splited = list(link.split('/'))

    return splited[2] if len(splited) > 2 else None

def get_price(link):
    # На основе ссылки на карточку товара в интернет магазине возвращает текущую стоимость
    html = get_html(link)
    domen = get_domen(link)

    # parser[domen](html)


if __name__ == '__main__':
    text = get_html(f'https://www.mvideo.ru/products/smartfon-apple-iphone-13-pro-max-128gb-alpine-green-30063190', 'www.mvideo.ru')
    print(type(text))
    with open('html.html', 'w', encoding="utf-8") as f:
        f.write(text)