from typing import Any
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from .models import CustomUser
from .forms import CustomUserCreationForm
from reservation.permissions import IsOwnerOrReadOnly, CanCreateUser
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
)
from rest_framework import permissions as permission
from rest_framework.permissions import IsAdminUser
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .mixins import CustomAuthorizationMixin, CustomLoginRequiredMixin

from django.urls import reverse_lazy

from .serializers import CustomUserSerializer, CustomUserCreateLessFieldsSerializer


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "home/register.html"
    success_url = reverse_lazy("reservation.list")
    model = CustomUser
    success_message = "Registration successful. you can now log in."

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("reservation.list")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class LogoutInterfaceView(LogoutView):
    template_name = "home/logout.html"


class LoginInterfaceView(LoginView):
    template_name = "home/login.html"


class HomeView(TemplateView):
    template_name = "home/welcome.html"
    extra_context = {"today": datetime.today()}


class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = "home/authorized.html"
    login_url = "/login"


class CustomUserDetailView(CustomLoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "home/user_detail.html"
    context_object_name = "user"


class UpdateView(CustomLoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "home/register.html"
    success_url = "/mini/reservation"
    form_class = CustomUserCreationForm

    success_message = "User updated successfully."

    def get(self, request, *args, **kwargs):
        print("user", type(request.user))

        pk = self.request.user.pk
        self.object = self.model.objects.get(pk=pk)
        form = CustomUserCreationForm(instance=self.object)
        return render(request, "home/register.html", {"form": form})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class CustomUserDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "home/user_delete.html"
    success_url = "/mini/reservation"
    success_message = "User deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CustomUserDeleteView, self).delete(request, *args, **kwargs)


# api'S


class CustomUserApiList(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CustomUserApiDetail(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CustomUserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateLessFieldsSerializer
    permission_classes = (CanCreateUser,)


    def perform_create(self, serializer):
        serializer.save()
