from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import ParkingPlace, Order, AppUser, BankCard, Сheque
from .forms import ParkingForm, OrderForm, CloseOrderForm, ProfileForm, BankCardForm
from .filters import ParkingPlaceFilter
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
# Create your views here.

#from django.contrib.postgres.search import SearchVector, SearchQuery, SearchHeadline
# from django.contrib.postgres.search import TrigramSimilarity


class MainPage(ListView):
    """Представление главной страницы"""
    model = ParkingPlace
    # ordering = '-creation_date'
    template_name = 'baseapp/main.html'                 # Относительный адрес шаблона
    context_object_name = 'demo_place_list'             # Имя для обращения в контексте

class ParkingList(ListView):
    """Представление каталога"""
    model = ParkingPlace                                # Имя модели
    template_name = 'baseapp/catalog.html'              # Относительный адрес шаблона
    context_object_name = 'parking_list'                # Имя для обращения в контексте
    ordering = ['pricePerHour']                        # Сортировка по убыванию цены
    paginate_by = 1                                     # поставим постраничный вывод в один элемент

    # забираем отфильтрованные объекты переопределяя метод get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = ParkingPlaceFilter(self.request.GET, queryset=self.get_queryset())
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return ParkingPlaceFilter(self.request.GET, queryset=queryset).qs





class SearchParking(ListView):
    """Представление поиска"""
    model = ParkingPlace                                # Имя модели
    template_name = 'search/search.html'                # Относительный адрес шаблона
    context_object_name = 'search_list'                 # Имя для обращения в контексте

class ParkingDetail(DetailView, CreateView):
    """Представление машино-места"""
    model = ParkingPlace
    template_name = 'baseapp/parking_detail.html'       # Относительный адрес шаблона
    context_object_name = 'parking_detail'              # Имя для обращения в контексте
    form_class = OrderForm                              # Имя формы

    def get_initial(self):
        """Переопределение функции для автозаполнения полей 'arendator' и 'parkingPlace' """
        initial = super().get_initial()
        user = self.request.user
        parkingPlace = ParkingPlace.objects.get(id=self.kwargs['pk'])
        initial['arendator'] = user
        initial['parkingPlace'] = parkingPlace
        return initial

class CreateParking(CreateView, LoginRequiredMixin):
    """Представление для создания машино-места."""
    model = ParkingPlace                                # Имя модели
    template_name = 'baseapp/create_parking.html'       # Относительный адрес шаблона
    form_class = ParkingForm                            # Имя формы

    def get_initial(self):
        """Переопределение функции для автозаполнения поля "автор объявления" """
        initial = super().get_initial()
        user = self.request.user
        initial['owner'] = user
        return initial

class UpdateParking(UpdateView, LoginRequiredMixin):
    """Представление для редактирования машино-места."""
    template_name = 'baseapp/edit_parking.html'         # Относительный адрес шаблона
    form_class = ParkingForm                            # Имя формы

    def get_object(self, **kwargs):
        """Метод get_object мы используем вместо queryset,
        чтобы получить информацию об объекте, который мы собираемся редактировать"""
        id = self.kwargs.get('pk')
        return ParkingPlace.objects.get(pk=id)

class DeleteParking(DeleteView, LoginRequiredMixin):
    """Представление для удаления машино-места."""
    template_name = 'baseapp/delete_parking.html'       # Относительный адрес шаблона
    queryset = ParkingPlace.objects.all()               # Кварисет (набор) объектов
    success_url = reverse_lazy('profile')               # Перенаправление после удаления

class Profile(TemplateView):
    """Представление профиля пользователя."""
    model = User                                        # Имя модели
    template_name = 'baseapp/profile.html'              # Относительный адрес шаблона
    form_class = ProfileForm                            # Имя формы

    def get_initial(self):
        """Переопределение функции для автозаполнения поля 'user' """
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
        context['profile'] = profile

        myCards = BankCard.objects.filter(owner=profile)
        context['my_cards'] = myCards

        myParkingPlaces = ParkingPlace.objects.filter(owner=profile)
        context['my_places'] = myParkingPlaces

        myBooking = Order.objects.filter(arendator=profile, orderState='ON')
        context['my_orders'] = myBooking

        myProfits = Сheque.objects.filter(beneficiary=profile)
        context['my_profits'] = myProfits

        return context

class EditProfile(UpdateView):
    """Представление для редактирования профиля пользователя."""
    template_name = 'baseapp/edit_profile.html'         # Относительный адрес шаблона
    form_class = ProfileForm                            # Имя формы

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return AppUser.objects.get(pk=id)

class OrderDetail(DetailView):
    """Представление брони машиноместа."""
    model = ParkingPlace                                # Имя модели
    template_name = 'baseapp/order_detail.html'         # Относительный адрес шаблона
    context_object_name = 'order_detail'                # Имя для обращения в контексте

class UpdateOrder(UpdateView):
    """Представление для завершения брони машиноместа."""
    template_name = 'baseapp/edit_order.html'           # Относительный адрес шаблона
    form_class = CloseOrderForm                         # Имя формы

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Order.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим список связанных с объявлением откликов'.
        this_order = Order.objects.get(pk=self.kwargs.get('pk'))
        context['time_now'] = timezone.now()
        rent_time = timezone.now() - this_order.creation_date  # вычисляем время аренды
        rent_hours = rent_time.seconds // 3600  # вычисляем часы аренды
        # if rent_hours == 0:
        #     rent_hours += 1
        rent_minutes = rent_time.seconds % 3600 // 60  # вычисляем минуты аренды
        price_per_hour = this_order.parkingPlace.pricePerHour  # извлекаем стоимость аренды за час
        price_hours = (rent_hours * price_per_hour)  # вычисляем стоимость арендованных часов
        price_per_min = (price_per_hour / 60)
        price_minutes = + (price_per_min * rent_minutes)  # вычисляем стоимость арендованных минут
        total_price = int(price_hours + price_minutes)  # вычисляем полную стоимость аренды
        context['this_order'] = this_order
        context['total_price'] = total_price

        return context

def stop_arendation(request, **kwargs):
    """Функция завершения брони машиноместа."""
    order = Order.objects.get(pk=kwargs['pk'])
    order.orderState =  'OFF'
    order.save(update_fields=["orderState"])

    return redirect(request.META.get('HTTP_REFERER', '/'))

class CreateBankCard(CreateView, LoginRequiredMixin):
    """Представление для создания банковской карты."""
    model = BankCard                                    # Имя модели
    template_name = 'baseapp/create_bankcard.html'      # Относительный адрес шаблона
    form_class = BankCardForm                           # Имя формы

    def get_initial(self):
        """Переопределение функции для автозаполнения поля owner"""
        initial = super().get_initial()
        user = self.request.user
        initial['owner'] = user
        return initial

class DeleteBankCard(DeleteView, LoginRequiredMixin):
    """Представление для удаления банковской карты."""
    template_name = 'baseapp/delete_bankcard.html'      # Относительный адрес шаблона
    queryset = BankCard.objects.all()                   # Кварисет (набор) схожих объектов
    success_url = reverse_lazy('profile')               # Перенаправление после удаления
