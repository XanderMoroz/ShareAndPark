from django.contrib import admin
from .models import ParkingPlace, AppUser, Order, BankCard, Сheque

# Register your models here.
admin.site.register(ParkingPlace)           # Подключаем к админке машино-места
admin.site.register(AppUser)                # Подключаем к админке профили пользователей
admin.site.register(Order)                  # Подключаем к админке брони машино-мест
admin.site.register(BankCard)               # Подключаем к админке банковские карты
admin.site.register(Сheque)                 # Подключаем к админке платежные чеки
