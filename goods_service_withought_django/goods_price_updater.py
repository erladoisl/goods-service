from modules.firebase import update_prices
from modules.config import project_path
import logging

logging.basicConfig(filename=f'{project_path}dtp.log', level=logging.INFO)

if __name__ == '__main__':
    update_prices()