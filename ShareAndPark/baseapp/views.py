from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import ParkingPlace, Order, AppUser
from .forms import ParkingForm, OrderForm, ProfileForm, ProfileOrderForm
from django.contrib.auth.models import User
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

class ParkingDetail(DetailView, CreateView):
    model = ParkingPlace
    # Используем шаблон — ad_detail.html
    template_name = 'baseapp/parking_detail.html'
    # Название объекта, в котором будет выбранное пользователем объявление
    context_object_name = 'parking_detail'
    form_class = OrderForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        parkingPlace = ParkingPlace.objects.get(id=self.kwargs['pk'])
        #author = Author.objects.get(user_id=user.pk)
        initial['arendator'] = user
        initial['parkingPlace'] = parkingPlace
        return initial



class CreateParking(CreateView, LoginRequiredMixin):
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

class Profile(TemplateView):
    model = User
    template_name = 'baseapp/profile.html'
    form_class = ProfileForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['user'] = user
        return initial

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим список связанных с объявлением откликов'.
        user = self.request.user
        profile = AppUser.objects.get(user=user)
        myParkingPlaces = ParkingPlace.objects.filter(owner=profile)
        myBooking = Order.objects.filter(arendator=profile)
        context['profile'] = profile
        context['my_places'] = myParkingPlaces
        context['my_orders'] = myBooking
        return context

class EditProfile(UpdateView):
    template_name = 'baseapp/edit_profile.html'
    form_class = ProfileForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return AppUser.objects.get(pk=id)


class OrderDetail(DetailView):
    model = ParkingPlace
    # Используем шаблон — ad_detail.html
    template_name = 'baseapp/order_detail.html'
    # Название объекта, в котором будет выбранное пользователем объявление
    context_object_name = 'order_detail'

class UpdateOrder(UpdateView):
    model = Order
    template_name = 'baseapp/edit_order.html'
    form_class = ProfileOrderForm