# from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.gis.forms import OSMWidget, PointField
from django.forms import ModelForm
from .models import ParkingPlace, Order, AppUser, BankCard


class ParkingForm(ModelForm):
    """ Форма для создания машино-места"""
    location = PointField(widget=
        OSMWidget(attrs={'map_width': 800,
                         'map_height': 500,
                         'default_lon': 37.618423,
                         'default_lat': 55.751244,
                         },
                  ))

    class Meta:
        """
        В класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
        Мы уже делали что-то похожее с фильтрами.
        """
        model = ParkingPlace
        fields = [
            'location',
            'title',
            'description',
            'pricePerHour',
            'readyToRent',
            'subway_station',
            'owner',
            'image',
                ]
        labels = {
            'title': "Адрес",
            'description': "Описание",
            'pricePerHour': "Цена за час",
            'readyToRent': "Статус парковочного места",
            'subway_station': "Ближайшее метро",
            'image': "Фотография парковочного места"
        }

        widgets = {'owner': forms.HiddenInput(),
                   'readyToRent': forms.HiddenInput()}

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
                   'orderState': forms.HiddenInput(),
                   'parkingPlace': forms.HiddenInput(),
                   }

class CloseOrderForm(ModelForm):
    """Форма для завершения брони"""
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
            'photo',
            'user',
            'name',
            'surname',
            'phoneNumber',
            'afertaSubmission',
        ]

        widgets = {'user': forms.HiddenInput(),
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
                   'balance': forms.HiddenInput()}

