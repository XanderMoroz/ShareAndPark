from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
# Create your models here.


class AppUser(models.Model):
    '''
    Модель Author, содержащая объекты всех авторов.
    Имеет следующие поля:
    - cвязь «один к одному» с встроенной моделью пользователей User;
    - рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='Имя')
    surname = models.CharField(max_length=128, verbose_name='Фамилия')
    phoneNumber = models.CharField(max_length=15, verbose_name='Номер телефона')
    afertaSubmission = models.BooleanField(verbose_name='Согласие с афертой')

    def __str__(self):
        return f'{self.user}'

class ParkingPlace(models.Model):
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name='Владелец')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=512, verbose_name='Описание')
    pricePerHour = models.IntegerField(verbose_name='Цена за час')
    latitude = models.FloatField(verbose_name='Широта', default=0.0)
    longitude = models.FloatField(verbose_name='Долгота', default=0.0)
    readyToRent = models.CharField(verbose_name='Статус',
                                   choices=[('ON', 'Готов к аренде'), ('OFF', 'Не готов к аренде')],
                                   default='OFF',
                                   max_length=3
                                   )

    def __str__(self):
        return f'{self.owner} {self.readyToRent}'

    def get_absolute_url(self):  # добавим путь, чтобы после создания перебрасывало на страницу с объявлениями.
        return f'/{self.id}'

class Order(models.Model):
    parkingPlace = models.ForeignKey(ParkingPlace, on_delete=models.CASCADE, verbose_name='Машино-место')
    orderState = models.CharField(verbose_name='Статус аренды',
                                  choices=[('ON', 'Арендуется'), ('OFF', 'Не арендуется')],
                                  default='OFF',
                                  max_length=3)
    arendator = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name='Арендатор')

    def __str__(self):
        return f'{self.parkingPlace} {self.orderState} {self.arendator}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse_lazy('parking_list')

class BankCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец карты')
    balance = models.IntegerField(verbose_name='Баланс', default=0)

    def __str__(self):
        return f'{self.owner}, {self.balance}'

