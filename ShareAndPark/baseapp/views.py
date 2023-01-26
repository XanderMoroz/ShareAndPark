from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import ParkingPlace
from .forms import ParkingForm
# Create your views here.

#from django.contrib.postgres.search import SearchVector, SearchQuery, SearchHeadline
# from django.contrib.postgres.search import TrigramSimilarity


class MainPage(ListView):
    model = ParkingPlace
    # ordering = '-creation_date'
    template_name = 'baseapp/main.html'
    context_object_name = 'demo_place_list'

class ParkingList(ListView):
    model = ParkingPlace
    template_name = 'baseapp/catalog.html'
    context_object_name = 'parking_list'

class SearchParking(ListView):
    model = ParkingPlace
    template_name = 'search/search.html'
    context_object_name = 'search_list'

class ParkingDetail(DetailView):
    model = ParkingPlace
    # Используем шаблон — ad_detail.html
    template_name = 'baseapp/parking_detail.html'
    # Название объекта, в котором будет выбранное пользователем объявление
    context_object_name = 'parking_detail'

class CreateParking(UpdateView, LoginRequiredMixin):
    """
    Класс представления для создания машино-места.
    Наследован от встроенного дженерика, миксина требующего авторизацию и миксина, требующего право доступа
    """
    model = ParkingPlace
    template_name = 'baseapp/create_parking.html'
    form_class = ParkingForm

    def get_initial(self):
        """
        Переопределение функции для автозаполнения поля "автор объявления"
        """
        initial = super().get_initial()
        user = self.request.user
        initial['user'] = user
        return initial

class UpdateParking(UpdateView, LoginRequiredMixin):
    template_name = 'baseapp/edit_parking.html'
    form_class = ParkingForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return ParkingPlace.objects.get(pk=id)

class DeleteParking(DeleteView, LoginRequiredMixin):
    """
    Класс представления для удаления объявления.
    Наследован от встроенного дженерика.
    """
    template_name = 'baseapp/delete_parking.html'
    queryset = ParkingPlace.objects.all()
    success_url = '/'
