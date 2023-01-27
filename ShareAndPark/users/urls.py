from django.urls import path
from .views import HomePage, BaseRegisterView

urlpatterns = [
    path('', HomePage.as_view(), name = "account"),                  # Главная страница
    path("signup/", BaseRegisterView.as_view(), name="signup"),                # Поиск машино-мест
]

