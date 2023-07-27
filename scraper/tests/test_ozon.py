from django.test import TestCase
import scraper.market.ozon as ozon


class OzonTestCase(TestCase):
    def test_parse_success(self):
        with open('scraper/tests/files/ozon/ozon_629.html', 'r') as f:
            text = f.read()
            result1 = ozon.parse(text)
            self.assertEqual(result1, 629)

        with open('scraper/tests/files/ozon/ozon_2780.html', 'r') as f:
            text = f.read()
            result1 = ozon.parse(text)
            self.assertEqual(result1, 2780)

    def test_page_not_exist(self):
        with open('scraper/tests/files/ozon/ozon_page_not_exists.html', 'r') as f:
            text = f.read()
            result1 = ozon.parse(text)
            self.assertEqual(result1, -1)

    def test_not_sales(self):
        with open('scraper/tests/files/ozon/ozon_not_sales.html', 'r') as f:
            text = f.read()
            result1 = ozon.parse(text)
            self.assertEqual(result1, -1)
