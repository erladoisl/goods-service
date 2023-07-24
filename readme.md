# Description:

Данный сервис актуализирует текущую цену о товарах в БД firebase проекта goods-gazer.
Задача обновления цен запускается раз в день.

# How to run

Update goods-gazer-firebase-adminsdk.json and modules/config.py by examples


### First run

- docker-compose up --build
- docker-compose run worker python manage.py createsuperuser

### Next run
- docker-compose up