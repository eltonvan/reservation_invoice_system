from typing import Any
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from reservation.mixins import CustomAuthorizationMixin, CustomLoginRequiredMixin
from django.http import HttpResponseRedirect




class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'home/register.html'
    success_url = '/mini/reservation'
    model = CustomUser
   # success_message = "Registration successful. you can now log in."
    


    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('reservation.list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)
    

    

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'


class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'


class HomeView(TemplateView):
    template_name = 'home/welcome.html'
    extra_context = {'today': datetime.today()}


class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/authorized.html'
    login_url = '/login'


class UpdateView(CustomAuthorizationMixin, UpdateView):
    model = CustomUser
    template_name = 'home/register.html'
    success_url = '/mini/reservation'
    form_class = CustomUserCreationForm
    
    success_message = "User updated successfully."



    def get(self, request, *args, **kwargs):
        print("user", type(request.user))

        pk = self.request.user.pk
        self.object = self.model.objects.get(pk=pk)
        form = CustomUserCreationForm(instance=self.object)
        return render(request, 'home/register.html', {"form": form})


    def form_valid(self, form):
        form.instance.user = self.request.user 
        form.save()
        return HttpResponseRedirect(self.get_success_url())



    