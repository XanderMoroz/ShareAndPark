from django_filters import FilterSet, CharFilter, NumberFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import ParkingPlace


# создаём фильтр
class ParkingPlaceFilter(FilterSet):
    price__gt = NumberFilter(label='Цена до', field_name='pricePerHour', lookup_expr='lt')
    # Здесь в мета классе надо предоставить модель и указать поля,
    # по которым будет фильтроваться (т. е. подбираться) информация о машино-местах
    class Meta:
        model = ParkingPlace
        fields = ('readyToRent',
                  # 'pricePerHour',
                  'subway_station',
                  )  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)