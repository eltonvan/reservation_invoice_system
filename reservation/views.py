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
from .forms import ReservationForm
from .models import Reservation


class ResDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation 
    success_url = '/mini/reservation'
    template_name = 'booking/res_delete.html'
    login_url = "/login"
    

class ResUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation 
    success_url = '/mini/reservation'
    form_class = ReservationForm
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

    # def form_valid(self, form: BaseModelForm) -> HttpResponse:
    #     self.object = form.save(commit=False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())


class ResListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'booking/res_list.html'
    context_object_name = 'reservation'
    login_url = "/login"
  
    def get_queryset(self):
        
        return self.request.user.reservation.all()



class ResDetailView(DetailView):
    model = Reservation
    context_object_name = 'reservation_list'
    login_url = "/login"



