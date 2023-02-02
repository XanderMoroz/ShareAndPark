# from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm
from .models import ParkingPlace, Order, AppUser, BankCard

class ParkingForm(ModelForm):
    """ Форма для создания машино-места"""
    # content = forms.CharField(widget=CKEditorWidget, label='Содержание объявления')
    class Meta:
        """
        В класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
        Мы уже делали что-то похожее с фильтрами.
        """
        model = ParkingPlace
        fields = [
            'title',
            'description',
            'pricePerHour',
            'readyToRent',
            'owner',
                ]
        labels = {
            'title': "Заголовок",
            'description': "Содержание",
            'pricePerHour': "Цена за час",
            'readyToRent': "Статус парковочного места",
        }

        widgets = {'owner': forms.HiddenInput()}

class OrderForm(ModelForm):
    """Форма для создания брони"""
    class Meta:
        model = Order
        fields = [
            'parkingPlace',
            'orderState',
            'arendator'
                ]

        widgets = {'arendator': forms.HiddenInput(),
                   # 'orderState': forms.HiddenInput(),
                   'parkingPlace': forms.HiddenInput(),
                   }

class ProfileForm(ModelForm):
    """Форма для создания профиля"""
    class Meta:
        model = AppUser
        fields = [
            'user',
            'name',
            'surname',
            'phoneNumber',
            'afertaSubmission',
        ]

        widgets = {'user': forms.HiddenInput(),
                   }

class ProfileOrderForm(ModelForm):
    """Форма для создания брони"""
    class Meta:
        model = Order
        fields = [
            'parkingPlace',
            'orderState',
            'arendator'
                ]

        widgets = {'arendator': forms.HiddenInput(),
                   # 'orderState': forms.HiddenInput(),
                   'parkingPlace': forms.HiddenInput(),
                   }

class BankCardForm(ModelForm):
    """Форма для создания банковской карты"""

    class Meta:
        model = BankCard
        fields = [
            'owner',
            'balance',
        ]

        widgets = {'owner': forms.HiddenInput(),
                   'balance': forms.HiddenInput(),
                   }