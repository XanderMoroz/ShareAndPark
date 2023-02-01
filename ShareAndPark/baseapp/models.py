from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
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

    class Meta:
        verbose_name = 'Машино-место'
        verbose_name_plural = 'Машино-места'

    def __str__(self):
        return f'Машино-место по адресу:{self.title}. Готов к аренде:{self.readyToRent}. Владелец:{self.owner} '

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse_lazy('profile')

class Order(models.Model):
    # creation_date = models.DateTimeField(auto_now_add=True)
    parkingPlace = models.ForeignKey(ParkingPlace, on_delete=models.CASCADE, verbose_name='Машино-место')
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
    # else:
    #     instance.parkingPlace.readyToRent = "ON"
    #     Bill.objects.create(user=instance)

# method for updating
@receiver(post_save, sender=Order, dispatch_uid="update_stock_count")
def hold_parkingPlace(sender, instance, **kwargs):
    if instance.orderState == "OFF":
        amount = instance.parkingPlace.pricePerHour
        print(amount)
        parkingPlaceOwner = instance.parkingPlace.owner
        print(parkingPlaceOwner)
        arendator_card = BankCard.objects.get(owner=instance.arendator)
        print(arendator_card)
        parkOwner_card = BankCard.objects.get(owner=parkingPlaceOwner)
        print(parkOwner_card)
        arendator_card.balance -= amount
        arendator_card.balance.save()
        parkOwner_card.balance += amount
        parkOwner_card.balance.save()


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
    beneficiary = models.ForeignKey(AppUser,
                                    on_delete=models.CASCADE,
                                    related_name='Сheque_beneficiary',
                                    verbose_name='Владелец карты')

    class Meta:
        verbose_name = 'Банковский чек'
        verbose_name_plural = 'Банковские чеки'

    def __str__(self):
        return f'Оплата парковки на сумму {self.amount}. Получатель {self.beneficiary}'

    @receiver(post_save, sender=Order)
    def create_cheque_and_payment(sender, instance, created, **kwargs):
        if not created:
            Сheque.objects.create(payer=instance.arendator,
                                  beneficiary=instance.parkingPlace.owner,
                                  amount=150
                                  )
            beneficiary = BankCard.objects.get(owner=instance.parkingPlace.owner)
            payer = BankCard.objects.get(owner=instance.arendator)
            beneficiary.balance += 150
            beneficiary.save(update_fields=["balance"])
            payer.balance -= 150
            payer.save(update_fields=["balance"])

