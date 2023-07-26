from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pyquery import PyQuery

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from scraper.market.util import save_file
from time import sleep
import logging
import traceback
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

class Request:
    selenium_retries = 0

    
    def __init__(self, url, domain):
        self.url = url
        self.domain = domain
        self.log = logging.getLogger('manage')
        self.log.addHandler(fh)
        self.log.setLevel(c.LOGGER_CONFIG['level'])
        
    def get_selenium_res(self, class_name):
        try:
            self.log.info(f'starting to get html {self.url}')
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value,
                                 OperatingSystem.LINUX.value]
            
            user_agent_rotator = UserAgent(software_names=software_names,
                                           operating_systems=operating_systems,
                                           limit=100)
            
            user_agent = user_agent_rotator.get_random_user_agent()
            
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1420, 1080')
            options.add_argument('--disable-gpu')
            options.add_argument('--user-agent={user_agent}')
            
            browser = webdriver.Chrome(options=options)
            browser.get(self.url)
            
            time_to_wait = 15
            
            try:
                WebDriverWait(browser, time_to_wait).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            finally:
                browser.maximize_window()
                page_html = browser.page_source
            
                if Request.make_captcha(page_html) and 'yandex' in self.domain:
                    self.log.info('Pass captcha required in yandex')
                    browser.find_element(By.CLASS_NAME, 'CheckboxCaptcha-Button').click()
                    sleep(15)
                    page_html = browser.page_source
                    
                browser.close()
                self.log.info(f'html page by {self.url} successfully got')
                save_file(self.domain, 'html', page_html, 'success')
                
                return page_html
        except (TimeoutError, WebDriverException):
            self.log.error(traceback.format_exc())
            sleep(6)
            self.selenium_retries += 1
            self.log.info('Selenium retry #: ' + str(self.selenium_retries))
            
            self.log.info(f'Retry to get html by {self.url}')
            
            return self.get_selenium_res(class_name)
        
    @staticmethod
    def make_captcha(html: str) -> bool:
        '''
            Проверка нужно ли пройти капчу от бота

            true если нужно пройти капчу

            >> make_captcha('<html prefix="og: http://ogp.me/ns#"><head><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ой!</title><meta data-react-helmet="true" property="og:title" content="Яндекс"><meta data-react-helmet="true" property="og:description" content="Найдётся всё"><meta data-react-helmet="true" property="og:image" content="https://yastatic.net/s3/home/logos/share/share-logo-ru.png"><link rel="stylesheet" href="/captcha_smart.min.css?k=1632998364813"></head><body class="utilityfocus"><div id="root"><div class="Theme Theme_color_yandex-default Theme_root_default"><div class="Container"><div class="Spacer" style="padding-bottom:40px"><a href="https://www.yandex.ru" title="Яндекс" class="Link Link_view_default LogoLink"><svg width="86" height="36" viewBox="0 0 86 36"><path d="M45.983 28.888H44.385L44.377 11.578H35.027V13.274C35.027 18.556 34.835 24.67 32.997 28.888H31.758V35.313H34.555V31.41H43.186V35.313H45.983V28.888ZM58.798 27.758C57.999 28.309 56.601 29.098 54.842 29.098C52.365 29.098 51.086 26.732 51.086 22.238H59.477V20.544C59.477 13.804 57.28 11.32 53.923 11.32C49.648 11.32 47.85 15.971 47.85 22.357C47.85 28.467 50.407 31.739 54.563 31.739C56.561 31.739 58.239 31.108 59.517 30.122L58.798 27.757V27.758ZM26.765 11.572V20.052H22.13V11.572H19.013V31.44H22.13V22.478H26.765V31.44H29.841V11.573H26.765V11.572ZM71.123 31.435H74.519L68.805 20.91L73.8 11.568H70.643L65.808 20.752V11.57H62.692V31.437H65.808V21.543L71.123 31.437V31.435ZM86.02 30.19L85.3 27.904C84.581 28.534 83.423 29.126 81.904 29.126C79.387 29.126 78.188 26.288 78.188 21.321C78.188 16.315 79.786 13.831 82.024 13.831C83.303 13.831 84.501 14.501 85.341 15.211L85.781 12.294C84.901 11.742 83.862 11.269 82.064 11.269C77.349 11.269 74.912 15.251 74.912 21.479C74.912 28.259 77.509 31.689 81.824 31.689C83.662 31.689 84.941 31.097 86.02 30.19ZM41.304 28.991H35.95C37.628 24.773 37.828 18.664 37.828 14.485V14.13H41.304V28.991ZM53.931 13.894C55.729 13.894 56.289 16.377 56.289 19.767H51.134C51.334 16.22 52.014 13.894 53.931 13.894Z" fill="black"></path><path d="M11.892 20.85V31.375H14.969V3.52698H10.374C5.85802 3.52698 2.06202 6.42198 2.06202 12.335C2.06202 16.553 3.74002 18.839 6.25802 20.1L0.903015 31.375H4.46002L9.33502 20.849H11.892V20.85ZM11.898 18.393H10.26C7.58302 18.393 5.38502 16.935 5.38502 12.402C5.38502 7.71098 7.78302 6.09498 10.26 6.09498H11.898V18.393Z" fill="#FF0000"></path></svg></a></div><div class="Spacer" style="padding-bottom:16px"><span class="Text Text_weight_medium Text_typography_headline-s">Подтвердите, что запросы отправляли вы, а не робот</span></div><span class="Text Text_weight_regular Text_typography_body-long-m">Нам очень жаль, но запросы с вашего устройства похожи на автоматические.&nbsp;<a href="https://yandex.ru/support/smart-captcha" class="Link Link_view_default">Почему это могло произойти?</a></span><div class="Spacer Spacer_auto-gap_bottom" style="padding-top:40px;padding-bottom:40px"><div class="CheckboxCaptcha" data-testid="checkbox-captcha"><form method="POST" action="/checkcaptcha?key=97848151-2d4fabf6-2134d391-abcddf17_2%2F1657888851%2F172e6f1f7ad9807aac773362a02b35ee_5c3542d9b1bd8259c24b944225b941d5&amp;retpath=aHR0cHM6Ly9tYXJrZXQueWFuZGV4LnJ1L3Byb2R1Y3QtLXZzdHJhaXZhZW1haWEtcG9zdWRvbW9lY2huYWlhLW1hc2hpbmEtd2Vpc3NnYXVmZi1iZHctNDUzMy1kLzc3NTE1MTAzMT9jcGM9cHUyU3pGdWdnczBkcW9QR0V3LTZ6c1pHRHN1Y0xPQ0R2TUFpU2lCbFNMWFNPQXp1TENFREtWM016M01xYmVIRFZCZExiVkNnbWlET2JobVVra0N0SndRVnQ1TXFXV3B3QUo2WUxvMkZYU0pyVnFtcWVxNlIxRERRcUxocWxoZlFhQS1LUDZETkNPT2Q1WU9MM2pvMjF6ME1ncW8yXzhnYUZsT1FIMUlLWlZjVUxUTWJzY1JvVEZHZW9MbVdYb0xBJnNrdT03NzUxNTEwMzEmb2ZmZXJpZD1RT3ZEYzlnSjk1TkhfM3JyYjlPWXZnJmNwYT0x_9d4fa56f056d223e6a78ed53413cb1ec&amp;u=54d05856-5c07fb3a-67b51699-9724ff71" class="CheckboxCaptcha-Form"><div class="CheckboxCaptcha-Inner"><div class="CheckboxCaptcha-Anchor"><input type="submit" class="CheckboxCaptcha-Button" value=""><div class="CheckboxCaptcha-Checkbox" aria-checked="false"><svg class="SvgIcon" width="24" height="24" viewBox="0 0 24 25" fill="none"><path d="M4 12.5L9.5 18.5L20 6.5" stroke="#000" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></path></svg></div></div><div class="CheckboxCaptcha-Label"><span class="Text Text_weight_regular Text_typography_control-xxl CheckboxCaptcha-LabelText">Я не робот</span><span class="Text Text_color_control-secondary Text_weight_regular Text_typography_control-l">Нажмите, чтобы продолжить</span></div></div><input hidden="" name="key" value="97848151-2d4fabf6-2134d391-abcddf17_2/1657888851/172e6f1f7ad9807aac773362a02b35ee_5c3542d9b1bd8259c24b944225b941d5"><input hidden="" name="rdata" value="ie6naDXhVC6BcQrqiDV3fohMlhKEQIC1jLsyWAP4NTre7qdqNeFUed9sbImbKWI9lkzNBOEVzbeO80dCQ/51Ot7up2w14VQMij801og1d36MTJYF7w2O5cLkdHAB6H400K3+ey29FyecOXObyyB3JdwPwEOmA82w0fwoZR/ufjTQrvR7Lb0XJ5w5c5vIKncl3A/AQ6YDzbDU/ChlH+5+NNCu83stvRcnnDlzm8gvdyXcD8BDpgPNsNf8KHcM92h93u6kYTXhECqDLzqViHtsPYAIzVywSsPwg+8wK16oNzqR/uRjNepPed8kbomZK3czmA2fEvkN3uvS7mogXaMrOt7upW014QI5mjlzm8ksdyXOHNlV7w2M5MLkICVBuXgv0PayK2K+WmmMZH2DkjV3e4hMlgTvDYvhwuR0cAHofjTQqPJ7La8EPopwfd2fO29ryBvJHOFL2PDa8yMpXbc5fMru/Hsn9RAqgy86l8x4OWzfTIASpxbN6JSsZ3RBuX4p0PagOHuoE2fNOW2bkG0nat9CjlXwDdWmkqt3PU/+LzrIuLQscvdULtp+Zd/LdSZ6lkzJBuEVm6CVuz4zCKw5Ioa+szw7+RNzzWYry998eT3fV44Kt12at8z8dCBPoX15nr+jdTW9RGnVKC3MzzV3eYlMllaiQ5y3zPx0JU+hb2qHqep7ce5UcYk9M8rPNXd5jEyWVqJDnLfM/HQmT6F9eZ6/o3U1vU5p1To+1dl8eT3cV44Kt12at8z8dSBPoX15nr+jdTW8RGnVOj7V2Xx5Pd1djgq3XZq3zPx1JU+hfXmev6N1NbxDadUoLczPNXd4jEyWRLFaiv7CuSUzV+9pbZfg5D4v+Uw/nSk6lYh+bD2AGt5FpgPNutH8KHcM92h93u6uazXhECqDLzqViHFmPYAIzVywSsPwiOowKwv6d2uX4OQxIvlMP50pOpWIcWM9gAjNXLBKw/CI6TArT9J3dJerpzU3shg9gD8+zcN2Oz2WTMQI4RWJs4ytdz1P8yI6yKqnNWS+WmmGbX2D3msgepZMxQLhFYmzjK13PU/yKDrIqqc1ZL5aaYZofYPMeDls30KOWfYN1bSBsmF0QbltOsju8Hck9Udpkg=="><input hidden="" name="d" value="8szGWRfbdkvvXF+5qhlVH7purDDDL+/S4N4SEW2bGxg="><input hidden="" name="k" value="1_1657888851_8721252182630264792_7fb270a162525ec293ce94b2f1ebd0a3"></form></div></div><span class="Text Text_color_ghost Text_weight_regular Text_typography_control-xs">Если у вас возникли проблемы, пожалуйста, воспользуйтесь&nbsp;<a href="https://yandex.ru/support/smart-captcha/#help" class="Link Link_view_default">формой обратной связи</a></span></div></div></div><script async="" src="https://mc.yandex.ru/metrika/tag.js"></script><script>window.__SSR_DATA__={url:"/ru/checkbox",reqId:"1657888851242668-3791934028789771851",invalid:"no",formAction:"/checkcaptcha?key=97848151-2d4fabf6-2134d391-abcddf17_2%2F1657888851%2F172e6f1f7ad9807aac773362a02b35ee_5c3542d9b1bd8259c24b944225b941d5&retpath=aHR0cHM6Ly9tYXJrZXQueWFuZGV4LnJ1L3Byb2R1Y3QtLXZzdHJhaXZhZW1haWEtcG9zdWRvbW9lY2huYWlhLW1hc2hpbmEtd2Vpc3NnYXVmZi1iZHctNDUzMy1kLzc3NTE1MTAzMT9jcGM9cHUyU3pGdWdnczBkcW9QR0V3LTZ6c1pHRHN1Y0xPQ0R2TUFpU2lCbFNMWFNPQXp1TENFREtWM016M01xYmVIRFZCZExiVkNnbWlET2JobVVra0N0SndRVnQ1TXFXV3B3QUo2WUxvMkZYU0pyVnFtcWVxNlIxRERRcUxocWxoZlFhQS1LUDZETkNPT2Q1WU9MM2pvMjF6ME1ncW8yXzhnYUZsT1FIMUlLWlZjVUxUTWJzY1JvVEZHZW9MbVdYb0xBJnNrdT03NzUxNTEwMzEmb2ZmZXJpZD1RT3ZEYzlnSjk1TkhfM3JyYjlPWXZnJmNwYT0x_9d4fa56f056d223e6a78ed53413cb1ec&u=54d05856-5c07fb3a-67b51699-9724ff71",captchaKey:"97848151-2d4fabf6-2134d391-abcddf17_2/1657888851/172e6f1f7ad9807aac773362a02b35ee_5c3542d9b1bd8259c24b944225b941d5",imageSrc:"",voiceSrc:"",introSrc:"",aesKey:"8szGWRfbdkvvXF+5qhlVH7purDDDL+/S4N4SEW2bGxg=",aesSign:"1_1657888851_8721252182630264792_7fb270a162525ec293ce94b2f1ebd0a3"}</script><script src="/captcha_smart_error.min.js?k=1632998364813" crossorigin=""></script><script src="https://yastatic.net/react/16.8.4/react-with-dom-and-polyfills.min.js" crossorigin=""></script><script src="/captcha_smart.min.js?k=1632998364813" crossorigin=""></script><script>!function(e,t,n,a,c){e.ym=e.ym||function(){(e.ym.a=e.ym.a||[]).push(arguments)},e.ym.l=+new Date,a=t.createElement(n),c=t.getElementsByTagName(n)[0],a.async=1,a.src="https://mc.yandex.ru/metrika/tag.js",c.parentNode.insertBefore(a,c)}(window,document,"script"),ym(10630330,"init",{clickmap:!0,trackLinks:!0,accurateTrackBounce:!0,webvisor:!0,ut:"noindex",params:{req_id:"1657888851242668-3791934028789771851"}})</script><noscript><div><img src="https://mc.yandex.ru/watch/10630330?ut=noindex" style="position:absolute;left:-9999px" alt=""></div></noscript><div><img src="https://adfstat.yandex.ru/captcha?req_id=1657888851242668-3791934028789771851" style="position:absolute;left:-9999px" alt=""></div></body></html>')
            True
            >>> 
            >>> make_captcha('<div class="_3NaXx _3k4zY yCb5m" data-tid="ca3255c7"><span data-autotest-value="39" data-autotest-currency="₽"><span>39 990</span>&nbsp;<span class="-B-PA">₽</span></span></div><div class="_3NaXx _3kWlK" data-tid="ca3255c7"><span data-autotest-value="39" data-autotest-currency="₽"><span>39 990</span>&nbsp;<span class="-B-PA">₽</span></span></div><div class="_3NaXx _3PwoB ffKan" data-tid="ca3255c7"><span data-autotest-value="44" data-autotest-currency="₽"><span>44 990</span>&nbsp;<span class="-B-PA">₽</span></span></div>')
            False
        '''
        pq = PyQuery(html)

        return len(pq('input.CheckboxCaptcha-Button')) > 0