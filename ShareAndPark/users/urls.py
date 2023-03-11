from django.urls import path
from .views import SignUp

urlpatterns = [
    # path('', HomePage.as_view(), name="account"),                  # Главная страница
    path("signup/", SignUp.as_view(), name="signup"),                # Поиск машино-мест
]

