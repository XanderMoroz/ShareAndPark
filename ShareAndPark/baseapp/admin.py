from django.contrib import admin
from .models import ParkingPlace, AppUser, Order, BankCard

# Register your models here.
admin.site.register(ParkingPlace)
admin.site.register(AppUser)
admin.site.register(Order)
admin.site.register(BankCard)