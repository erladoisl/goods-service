from django.test import TestCase
import scraper.market.yandex as yandex


class YandexTestCase(TestCase):
    def test_parse_few_suggestions_success(self):
        with open('scraper/tests/files/yandex/few_suggestions.html', 'r') as f:
            text = f.read()
            result1 = yandex.parse(text)
            self.assertEqual(result1, 4340)

    def test_parse_min_price_in_another_suggestion_success(self):
        with open('scraper/tests/files/yandex/min_price_in_another_suggestion.html', 'r') as f:
            text = f.read()
            result1 = yandex.parse(text)
            self.assertEqual(result1, 1850)


    def test_parse_not_saves_success(self):
        with open('scraper/tests/files/yandex/not_saves.html', 'r') as f:
            text = f.read()
            result1 = yandex.parse(text)
            self.assertEqual(result1, -1)

    def test_parse_one_suggestion_your_price_success(self):
        with open('scraper/tests/files/yandex/one_suggestion_your_price.html', 'r') as f:
            text = f.read()
            result1 = yandex.parse(text)
            self.assertEqual(result1, 4242)

    def test_simple_one_suggestion_success(self):
        with open('scraper/tests/files/yandex/simple_one_suggestion.html', 'r') as f:
            text = f.read()
            result1 = yandex.parse(text)
            self.assertEqual(result1, 2090)
