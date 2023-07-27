from django.test import TestCase
import scraper.market.mvideo as mvideo


class MvideoTestCase(TestCase):
    def test_parse_success(self):
        with open('scraper/tests/files/mvideo/mvideo_8100.html', 'r') as f:
            text = f.read()
            result1 = mvideo.parse(text)
            self.assertEqual(result1, 8100)

    def test_not_sales(self):
        with open('scraper/tests/files/mvideo/mvideo_not_sales.html', 'r') as f:
            text = f.read()
            result1 = mvideo.parse(text)
            self.assertEqual(result1, -1)
