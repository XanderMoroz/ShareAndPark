from django.contrib.auth.models import User
from .models import AppUser, ParkingPlace, Order, BankCard, Сheque
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Сигнал для привязки профиля к новому пользователю"""
    if created:
        AppUser.objects.create(user=instance)


@receiver(post_save, sender=Order, dispatch_uid="update_stock_count")
def hold_parkingPlace(sender, instance, created,  **kwargs):
    """В момент начала аренды статуса машино-места меняется на "Не готов к аренде". """
    if created:
        instance.parkingPlace.readyToRent = "OFF"
        instance.parkingPlace.save()


@receiver(post_save, sender=Order)
def create_cheque_and_payment(sender, instance, created, **kwargs):
    """В момент начала аренды статуса машино-места меняется на "Не готов к аренде". """
    if not created:  # если бронь не создана только что, а обновлена

        """В момент окончания аренды статус машино-места меняется на "Готов к аренде". """
        parking = ParkingPlace.objects.get(owner=instance.parkingPlace.owner)
        parking.readyToRent = "ON"  # и делаем его доступной для новой аренды
        parking.save(update_fields=["readyToRent"])

        rent_time = timezone.now() - instance.creation_date     # вычисляем время аренды
        rent_hours = rent_time.seconds // 3600                  # вычисляем часы аренды
        if rent_hours == 0:
            rent_hours += 1
        rent_minutes = rent_time.seconds % 3600 // 60           # вычисляем минуты аренды
        price_per_hour = instance.parkingPlace.pricePerHour     # извлекаем стоимость аренды за час
        price_hours = (rent_hours * price_per_hour)             # вычисляем стоимость арендованных часов
        price_per_min = (price_per_hour / 60)
        price_minutes = + (price_per_min * rent_minutes)        # вычисляем стоимость арендованных минут
        total_price = int(price_hours + price_minutes)          # вычисляем полную стоимость аренды

        """Создаем чек с вычисленной стоимостью аренды"""
        Сheque.objects.create(payer=instance.arendator,
                              beneficiary=instance.parkingPlace.owner,
                              amount=total_price)

        # извлекаем карту владельца машиноместа
        beneficiary_card = BankCard.objects.get(owner=instance.parkingPlace.owner)
        beneficiary_card.balance += total_price                             # начисляем средства на баланс
        beneficiary_card.save(update_fields=["balance"])                    # обновляем баланс
        # извлекаем карту арендатора
        payer_card = BankCard.objects.get(owner=instance.arendator)
        payer_card.balance -= total_price                                   # начисляем средства на баланс
        payer_card.save(update_fields=["balance"])                          # обновляем баланс
