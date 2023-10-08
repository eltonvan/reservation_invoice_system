
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReservationForm, PlatformForm, ApartmentForm, TaxRateForm
from .models import Reservation, Platform, Apartment, TaxRate, Invoice
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import F

RESERVATION_URL = "/mini/reservation"
LOGIN_URL = "/login"
PLATFORM_URL = "/mini/platform"
APARTMENT_URL = "/mini/apartment"
TAX_RATE_URL = "/mini/taxrate"




# view of reservation pages
class ResDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    success_url = RESERVATION_URL
    template_name = "booking/res_delete.html"
    login_url = LOGIN_URL


class ResUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    success_url = RESERVATION_URL
    form_class = ReservationForm
    template_name = "booking/res_form.html"
    login_url = LOGIN_URL


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReservationForm(instance=self.object, user=request.user)
        return render(request, "booking/res_form.html", {"form": form})

    def form_valid(self, form):
        form.instance.user = self.request.user 
        form.save()
        return HttpResponseRedirect(self.get_success_url())




class ResCreateView(LoginRequiredMixin, CreateView):

    model = Reservation
    template_name = "booking/res_form.html"
    success_url = RESERVATION_URL


    fields = [
            "start_date",
            "end_date",
            "name",
            "lname",
            "t_sum",
            "address",
            "commission",
            "rech_num",
            "purpose",
            "number_of_guests",
            "apartment",
            "platform",
            "company",
            "email",
            "nationality",
            "comment",
           
        ]

    def get(self, request, *args, **kwargs):
        form = ReservationForm(user=request.user)
        print("print on view", request.user)
        return render(request, "booking/res_form.html", {"form": form})
    


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    





class ResListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "booking/res_list.html"
    context_object_name = "reservation"
    login_url = LOGIN_URL

    def get_queryset(self):
        queryset =  self.request.user.reservation.order_by(F('start_date').asc())

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        name = self.request.GET.get('name')

        
        if start_date and end_date:
            queryset = queryset.filter(start_date__gte=start_date, end_date__lte=end_date)

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
class ResDetailView(DetailView):
    model = Reservation
    template_name = "booking/res_detail.html"
    context_object_name = "res"


# platform pages


class PltListView(LoginRequiredMixin, ListView):
    model = Platform
    template_name = "platform/plt_list.html"
    context_object_name = "platform"
    login_url = LOGIN_URL

    def get_queryset(self):
        return self.request.user.platform.all()


class PltDetailView(LoginRequiredMixin, DetailView):
    model = Platform
    template_name = "platform/plt_detail.html"
    context_object_name = "plt"
    login_url = "/login"


class PltCreateView(LoginRequiredMixin, CreateView):
    model = Platform
    template_name = "platform/plt_form.html"
    success_url = PLATFORM_URL
    form_class = PlatformForm
    login_url = LOGIN_URL

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PltUpdateView(LoginRequiredMixin, UpdateView):
    model = Platform
    template_name = "platform/plt_form.html"
    success_url = PLATFORM_URL
    form_class = PlatformForm
    login_url = LOGIN_URL


class PltDeleteView(LoginRequiredMixin, DeleteView):
    model = Platform
    success_url = PLATFORM_URL
    template_name = "platform/plt_delete.html"
    login_url = LOGIN_URL


# apartment pages


class AptListView(LoginRequiredMixin, ListView):
    model = Apartment
    template_name = "apartment/apt_list.html"
    context_object_name = "apartment"  # name used in template

    def get_queryset(self):
        return self.request.user.apartment.all()


class AptDetailView(LoginRequiredMixin, DetailView):
    model = Apartment
    template_name = "apartment/apt_detail.html"
    context_object_name = "apt"  # name used in template
    login_url = LOGIN_URL


class AptCreateView(LoginRequiredMixin, CreateView):
    model = Apartment
    template_name = "apartment/apt_form.html"
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
    template_name = "apartment/apt_form.html"
    success_url = APARTMENT_URL
    form_class = ApartmentForm
    login_url = LOGIN_URL


class AptDeleteView(LoginRequiredMixin, DeleteView):
    model = Apartment
    success_url = APARTMENT_URL
    template_name = "apartment/apt_delete.html"
    login_url = LOGIN_URL

# taxRate pages


class TaxRateListView(LoginRequiredMixin, ListView):
    model = TaxRate
    template_name = "settings/tax_list.html"
    context_object_name = "taxrates"  # name used in template
    login_url = LOGIN_URL

    def get_queryset(self):
        #return TaxRate.objects.all()
        return self.request.user.taxrates.all()
        
    
    
class TaxRateDetailView(LoginRequiredMixin, DetailView):
    model = TaxRate
    template_name = "settings/tax_detail.html"
    context_object_name = "taxrate"  # name used in template
    login_url = LOGIN_URL


class TaxRateCreateView(LoginRequiredMixin, CreateView):
    model = TaxRate
    template_name = "settings/tax_form.html"
    success_url = TAX_RATE_URL
    form_class = TaxRateForm
    login_url = LOGIN_URL

    def form_valid(self, form): 
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    

class TaxRateUpdateView(LoginRequiredMixin, UpdateView):
    model = TaxRate
    template_name = "settings/tax_form.html"
    success_url = TAX_RATE_URL
    form_class = TaxRateForm
    login_url = LOGIN_URL


# invoice pages



    # model = Reservation
    # template_name = "invoice/inv_list.html"
    # context_object_name = "reservation"  # name used in template
    # login_url = LOGIN_URL

    # def get_queryset(self):
    #     return self.request.user.reservation.all()


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "invoice/inv_list.html"
    context_object_name = "invoices"
    login_url = LOGIN_URL
   # paginate_by = 1  # Set the number of invoices per page

    def get_queryset(self):
        invoices = Invoice.objects.filter(reservation__user=self.request.user)
        print(invoices)
        return invoices

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     invoices = context['invoices']

    #     paginator = Paginator(invoices, self.paginate_by)
    #     page_number = self.request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)

    #     context['invoices'] = page_obj

    #     # Add previous and next buttons to the context
    #     current_page_number = page_obj.number
    #     total_pages = paginator.num_pages
    #     context['has_previous'] = current_page_number > 1
    #     context['previous_page_number'] = current_page_number - 1 if current_page_number > 1 else None
    #     context['has_next'] = current_page_number < total_pages
    #     context['next_page_number'] = current_page_number + 1 if current_page_number < total_pages else None

    #     return context

# invoice as a list, takes data from reservation and calculates the fields on the fly. no invoice number
# wrong approach, invoice should be a separate model, see InvoiceDetailedView
class InvoiceDetailView(DetailView):
    model = Reservation
    template_name = "invoice/inv_detail.html"
    context_object_name = "reservation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.object

        # Calculate the required fields
        number_of_nights = (reservation.end_date - reservation.start_date).days
        citytax = reservation.calculate_citytax()
        vat = reservation.calculate_vat()
        netto = reservation.calculate_netto()

        # Add the calculated fields to the context
        context['number_of_nights'] = number_of_nights
        context['citytax'] = citytax
        context['vat'] = vat
        context['netto'] = netto

        return context
#invoice as a table
class InvoiceDetailedView(DetailView):
    model = Invoice
    template_name = "invoice/inv_detail1.html"
    context_object_name = "invoices"

    def get_template_names(self):
        invoice = self.get_object()
        reservation = invoice.reservation

        if self.request.user.country == 'Poland':
            return ["invoice/inv_detail.html"]
        else:
            return ["invoice/inv_detail1.html"]
    



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = self.object
        reservation = invoice.reservation

        context['invoices'] = invoice
        context['reservation'] = reservation

        return context



 
