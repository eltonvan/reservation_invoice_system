from typing import Any, List
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReservationForm, PlatformForm, ApartmentForm
from .models import Reservation, Platform, Apartment ,Invoice

RESERVATION_URL = '/mini/reservation'
LOGIN_URL = "/login"
PLATFORM_URL = '/mini/platform'
APARTMENT_URL = '/mini/apartment'
# view of reservation pages
class ResDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation 
    success_url = RESERVATION_URL
    template_name = 'booking/res_delete.html'
    login_url = LOGIN_URL
    

class ResUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation 
    success_url = RESERVATION_URL
    form_class = ReservationForm
    template_name = 'booking/res_form.html'
    login_url = LOGIN_URL

class ResCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'booking/res_form.html'
    success_url = RESERVATION_URL
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
    login_url = LOGIN_URL
  
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
    login_url = LOGIN_URL
    
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
    success_url = PLATFORM_URL
    form_class = PlatformForm
    login_url =LOGIN_URL

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PltUpdateView(LoginRequiredMixin, UpdateView):
    model = Platform
    template_name = 'platform/plt_form.html'
    success_url = PLATFORM_URL
    form_class = PlatformForm
    login_url =LOGIN_URL

class PltDeleteView(LoginRequiredMixin, DeleteView):
    model = Platform
    success_url = PLATFORM_URL
    template_name = 'platform/plt_delete.html'
    login_url = LOGIN_URL

# apartment pages

class AptListView(LoginRequiredMixin, ListView):
    model = Apartment
    template_name = 'apartment/apt_list.html'
    context_object_name = 'apartment' # name used in template
    
    def get_queryset(self):
        
        return self.request.user.apartment.all()
    
class AptDetailView(LoginRequiredMixin, DetailView):
    model = Apartment
    template_name = 'apartment/apt_detail.html'
    context_object_name = 'apt' # name used in template
    login_url = LOGIN_URL    



class AptCreateView(LoginRequiredMixin, CreateView):
    model = Apartment
    template_name = 'apartment/apt_form.html'
    success_url = APARTMENT_URL
    form_class = ApartmentForm
    login_url = LOGIN_URL

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
class AptUpdateView(LoginRequiredMixin, UpdateView):
    model = Apartment
    template_name = 'apartment/apt_form.html'
    success_url = APARTMENT_URL
    form_class = ApartmentForm
    login_url = LOGIN_URL

class AptDeleteView(LoginRequiredMixin, DeleteView):
    model = Apartment
    success_url = APARTMENT_URL
    template_name = 'apartment/apt_delete.html'
    login_url = LOGIN_URL

# invoice pages

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'invoice/inv_list.html'
    context_object_name = 'invoices' # name used in template
    login_url = LOGIN_URL
    
    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        queryset = super().get_queryset()

        if start_date and end_date:
            queryset = QuerySet.filter(date__range=[start_date, end_date])
        
        return queryset
    
class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'invoice/inv_detail.html'
    context_object_name = 'inv' # name used in template
    login_url = LOGIN_URL

    def get_object(self):
        reservation_id = self.kwargs.get('id')
        reservation = Reservation.objects.get(id=reservation_id)

        invoice = Invoice()
        invoice.calculate_fields(reservation)

        return invoice

