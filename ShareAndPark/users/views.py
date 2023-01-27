from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import BaseRegisterForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'users/home.html'

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = "registration/signup.html"
    success_url = '/'

# class SignUp(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"