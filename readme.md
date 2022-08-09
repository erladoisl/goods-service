# Описание сервиса

Данный сервис актуализирует текущую цену о товарах в БД firebase проекта goods-gazer.

Для обновления цен запускается модуль goods_price_updater, расположенный в корневой папке.

Рекомендованная частота обновления: раз в день.

# Requirements

1. python v 3.8.10
2. sudo apt install python3-venv
3. python -m venv goods_service_env
4. source goods_service_env/bin/activate
5. pip install -r requirements.txt

# How to run

1. update goods-gazer-firebase-adminsdk.json and modules/config.py by examples
2. python goods_price_updater

# cron settings

1. to run script every 5 mins:

*/5 * * * * /home/rakhina/goods_service/firebase/bin/python   /home/rakhina/goods_service/goods_price_updater.py
