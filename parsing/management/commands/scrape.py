from parsing.parsing.firebase import update_prices
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "run parse goods price"   

    def handle(self, *args, **options):
        update_prices()
