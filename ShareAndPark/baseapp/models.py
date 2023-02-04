from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime
import re

# Create your models here.


class AppUser(models.Model):
    '''
    Модель AppUser, содержащая объекты всех авторов.
    Имеет следующие поля:
    - cвязь «один к одному» с встроенной моделью пользователей User;
    - рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='Имя')
    surname = models.CharField(max_length=128, verbose_name='Фамилия')
    phoneNumber = models.CharField(max_length=15, verbose_name='Номер телефона')
    afertaSubmission = models.BooleanField(verbose_name='Согласие с афертой', default=True,)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            AppUser.objects.create(user=instance)

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse_lazy('profile')

    def __str__(self):
        return f'{self.user}'

class ParkingPlace(models.Model):
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name='Владелец')
    subway_station = models.CharField(verbose_name='Ближайшее метро',
                                      choices=[('KSM', 'Комсомольская'), ('KRS', 'Курская')],
                                      default='KSM',
                                      max_length=3)
    title = models.CharField(max_length=200, verbose_name='Адрес')
    description = models.CharField(max_length=512, verbose_name='Описание')
    pricePerHour = models.IntegerField(verbose_name='Цена за час')
    latitude = models.FloatField(verbose_name='Широта', default=0.0)
    longitude = models.FloatField(verbose_name='Долгота', default=0.0)
    readyToRent = models.CharField(verbose_name='Статус',
                                   choices=[('ON', 'Готов к аренде'), ('OFF', 'Не готов к аренде')],
                                   default='ON',
                                   max_length=3
                                   )

    class Meta:
        verbose_name = 'Машино-место'
        verbose_name_plural = 'Машино-места'

    def __str__(self):
        return f'Машино-место по адресу:{self.title}. Готов к аренде:{self.readyToRent}. Владелец:{self.owner} '

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse_lazy('profile')

class Order(models.Model):
    parkingPlace = models.ForeignKey(ParkingPlace, on_delete=models.CASCADE, verbose_name='Машино-место')
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    orderState = models.CharField(verbose_name='Статус аренды',
                                  choices=[('ON', 'Арендуется'), ('OFF', 'Аренда завершена')],
                                  default='ON',
                                  max_length=3)
    arendator = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name='Арендатор')

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def __str__(self):
        return f'{self.parkingPlace} {self.orderState} {self.arendator}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse_lazy('profile')

# обработчик сигнала
@receiver(post_save, sender=Order, dispatch_uid="update_stock_count")
def hold_parkingPlace(sender, instance, created,  **kwargs):
    if created:
        instance.parkingPlace.readyToRent = "OFF"
        instance.parkingPlace.save()

class BankCard(models.Model):
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name='Владелец карты')
    balance = models.IntegerField(verbose_name='Баланс', default=1000)

    class Meta:
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'

    def __str__(self):
        return f'{self.owner}, {self.balance}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse_lazy('profile')

class Сheque(models.Model):
    payer = models.ForeignKey(AppUser,
                              on_delete=models.CASCADE,
                              related_name='Сheque_payer',
                              verbose_name='Плательщик')
    amount = models.IntegerField(default=333, verbose_name='Стоимость парковки')
    creation_date = models.DateTimeField(auto_now_add=True)
    beneficiary = models.ForeignKey(AppUser,
                                    on_delete=models.CASCADE,
                                    related_name='Сheque_beneficiary',
                                    verbose_name='Владелец карты')

    class Meta:
        verbose_name = 'Банковский чек'
        verbose_name_plural = 'Банковские чеки'

    @receiver(post_save, sender=Order)
    def create_cheque_and_payment(sender, instance, created, **kwargs):
        if not created: # если бронь не создана только что, а обновлена

            # Освобождаем машино-место
            parking = ParkingPlace.objects.get(owner=instance.parkingPlace.owner)
            parking.readyToRent = "ON"  # и делаем его доступной для новой аренды
            parking.save(update_fields=["readyToRent"])

            rent_time = timezone.now() - instance.creation_date         #  вычисляем время аренды
            rent_hours = rent_time.seconds // 3600                      # вычисляем часы аренды
            if rent_hours == 0:
                rent_hours += 1
            rent_minutes = rent_time.seconds % 3600 // 60               # вычисляем минуты аренды
            price_per_hour = instance.parkingPlace.pricePerHour         # извлекаем стоимость аренды за час
            price_hours = (rent_hours * price_per_hour)                 # вычисляем стоимость арендованных часов
            price_per_min = (price_per_hour / 60)
            price_minutes = + (price_per_min * rent_minutes)            # вычисляем стоимость арендованных минут
            total_price = int(price_hours + price_minutes)              # вычисляем полную стоимость аренды

            Сheque.objects.create(payer=instance.arendator,
                                  beneficiary=instance.parkingPlace.owner,
                                  amount=total_price
                                  )


            beneficiary_card = BankCard.objects.get(owner=instance.parkingPlace.owner)
            payer_card = BankCard.objects.get(owner=instance.arendator)

            beneficiary_card.balance += total_price
            beneficiary_card.save(update_fields=["balance"])
            payer_card.balance -= total_price
            payer_card.save(update_fields=["balance"])


    def __str__(self):
        return f'Оплата парковки на сумму {self.amount}. Получатель {self.beneficiary}'


