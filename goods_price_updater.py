from datetime import datetime
from modules.firebase import update_prices
from modules.config import project_path
import logging

logging.basicConfig(filename=f'{project_path}dtp.log', level=logging.INFO)

if __name__ == '__main__':
    logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nНачало процесса получения актуальных цен')
    update_prices()