# from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm
from .models import ParkingPlace

class ParkingForm(ModelForm):
    """
    Форма для создания объявления
    """
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

# class FeedbackForm(ModelForm):
#     """
#     Форма для создания отклика на объявление
#     """
#     class Meta:
#         model = Feedback
#         fields = [
#             'text',
#             'ad',
#             'author'
#                 ]
#         labels = {
#             'text': "Текст отклика",
#         }
#
#         widgets = {'author': forms.HiddenInput(),
#                    'ad': forms.HiddenInput(),
#                    }
