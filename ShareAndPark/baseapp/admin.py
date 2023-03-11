from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import ParkingPlace, AppUser, Order, BankCard, Сheque
from leaflet.admin import LeafletGeoAdmin

@admin.register(ParkingPlace)
class ParkingPlaceAdmin(GISModelAdmin, LeafletGeoAdmin):
    list_display = ('location',)

    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 8,
            'default_lat': 50.324422739309384,
            'default_lon': 8.887939453125,
        },
    }


# Register your models here.
# admin.site.register(ParkingPlace)           # Подключаем к админке машино-места
admin.site.register(AppUser)                # Подключаем к админке профили пользователей
admin.site.register(Order)                  # Подключаем к админке брони машино-мест
admin.site.register(BankCard)               # Подключаем к админке банковские карты
admin.site.register(Сheque)                 # Подключаем к админке платежные чеки
