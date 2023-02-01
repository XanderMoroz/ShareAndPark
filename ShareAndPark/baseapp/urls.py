from django.urls import path
from .views import (
    SearchParking,
    MainPage,
    ParkingList,
    ParkingDetail,
    CreateParking,
    UpdateParking,
    DeleteParking,
    Profile,
    EditProfile,
    stop_arendation,
    CreateBankCard,
    DeleteBankCard
)


urlpatterns = [
    path('', MainPage.as_view(), name='welcome page'),                          # Главная страница
    path('search', SearchParking.as_view(), name='search_list'),                # Поиск машино-мест
    path('catalog', ParkingList.as_view(), name='parking_list'),                # Каталог машино-мест
    path('<int:pk>', ParkingDetail.as_view(), name='parking_detail'),           # Страница машино-места
    path('create', CreateParking.as_view(), name='create_parking'),             # Создать машино-место
    path('edit/<int:pk>', UpdateParking.as_view(), name='update_parking'),      # Редактировать машино-место
    path('delete/<int:pk>', DeleteParking.as_view(), name='delete_parking'),    # Удалить машино-место

    path('profile', Profile.as_view(), name='profile'),    # Удалить машино-место
    path('edit_profile/<int:pk>', EditProfile.as_view(), name='edit_profile'),  # Удалить машино-место
    # path('profile/edit_profile/<int:pk>', UpdateOrder.as_view(), name='update_order'),  # Удалить машино-место
    path('create_bankcard', CreateBankCard.as_view(), name='create_bankcard'),
    path('delete_bankcard/<int:pk>', DeleteBankCard.as_view(), name='delete_bankcard'),
    path('stop_arenda/<int:pk>', stop_arendation, name='stop_arendation'),
]