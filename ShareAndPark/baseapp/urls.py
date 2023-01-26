from django.urls import path
from .views import SearchParking, MainPage, ParkingList, ParkingDetail, CreateParking, UpdateParking, DeleteParking

urlpatterns = [
    path('', MainPage.as_view(), name='welcome page'),                          # Главная страница
    path('search', SearchParking.as_view(), name='search_list'),                # Поиск машино-мест
    path('catalog', ParkingList.as_view(), name='parking_list'),                # Каталог машино-мест
    path('<int:pk>', ParkingDetail.as_view(), name='parking_detail'),           # Страница машино-места
    path('create', CreateParking.as_view(), name='create_parking'),             # Создать машино-место
    path('edit/<int:pk>', UpdateParking.as_view(), name='update_parking'),      # Редактировать машино-место
    path('delete/<int:pk>', DeleteParking.as_view(), name='delete_parking'),    # Удалить машино-место

]