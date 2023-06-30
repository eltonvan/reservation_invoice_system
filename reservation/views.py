from typing import Any, List
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
#from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from datetime import datetime
#from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReservationForm, PlatformForm
from .models import Reservation, Platform

# view of reservation pages
class ResDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation 
    success_url = '/mini/reservation'
    template_name = 'booking/res_delete.html'
    login_url = "/login"
    

class ResUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation 
    success_url = '/mini/reservation'
    form_class = ReservationForm
    template_name = 'booking/res_form.html'
    login_url = "/login"

class ResCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'booking/res_form.html'
    success_url = '/mini/reservation'
    form_class = ReservationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())




class ResListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'booking/res_list.html'
    context_object_name = 'reservation'
    login_url = "/login"
  
    def get_queryset(self):
        
        return self.request.user.reservation.all()



class ResDetailView(DetailView):
    model = Reservation
    template_name = 'booking/res_detail.html'
    context_object_name = 'res'

# platform pages
    
class PltListView(LoginRequiredMixin, ListView):
    model = Platform
    template_name = 'platform/plt_list.html'
    context_object_name = 'platform'
    login_url = "/login"
    
    def get_queryset(self):
        
        return self.request.user.platform.all()


class PltDetailView(LoginRequiredMixin, DetailView):
    model = Platform
    template_name = 'platform/plt_detail.html'
    context_object_name = 'plt'
    login_url = "/login"

class PltCreateView(LoginRequiredMixin, CreateView):
    model = Platform
    template_name = 'platform/plt_form.html'
    success_url = '/mini/platform'
    form_class = PlatformForm
    login_url = "/login"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PltUpdateView(LoginRequiredMixin, UpdateView):
    model = Platform
    template_name = 'platform/plt_form.html'
    success_url = '/mini/platform'
    form_class = PlatformForm
    login_url = "/login"

class PltDeleteView(LoginRequiredMixin, DeleteView):
    model = Platform
    success_url = '/mini/platform'
    template_name = 'platform/plt_delete.html'
    login_url = "/login"
    