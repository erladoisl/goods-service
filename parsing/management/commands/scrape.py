from parsing.parsing.firebase import update_prices
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "collect jobs"   

    def handle(self, *args, **options):
        update_prices()

