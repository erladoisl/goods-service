import logging

token = '***'
project_path = '/home/rakhina/goods-service/'
chromedriver_path = f'{project_path}modules/chromedriver_windows.exe'
firebase_admin_sdk_path = f'{project_path}goods-gazer-firebase-adminsdk.json'

DB_NAME = 'golden-eye.db'

LOGGER_CONFIG = dict(level=logging.DEBUG,
                     file='app.log',
                     formatter=logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s:%(message)s'))


LOCATION_ACCURACY = 100
DEFAULT_LATITUDE = 55.783963
DEFAULT_LONGITUDE = 49.127415