from django.test import TestCase
import scraper.market.eldorado as eldorado


class EldoradoTestCase(TestCase):
    def test_parse_success(self):
        with open('scraper/tests/files/eldorado/eldorado_1999.html', 'r') as f:
            text = f.read()
            result1 = eldorado.parse(text)
            self.assertEqual(result1, 1999)

        with open('scraper/tests/files/eldorado/eldorado_32999.html', 'r') as f:
            text = f.read()
            result1 = eldorado.parse(text)
            self.assertEqual(result1, 32999)

    def test_not_sales(self):
        with open('scraper/tests/files/eldorado/eldorado_not_sales.html', 'r') as f:
            text = f.read()
            result1 = eldorado.parse(text)
            self.assertEqual(result1, -1)
