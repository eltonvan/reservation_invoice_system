from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReservationForm, PlatformForm, ApartmentForm, TaxRateForm, ReportForm
from .models import Reservation, Platform, Apartment, TaxRate, Invoice
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .utils import render_to_pdf, get_invoice_context
from .mixins import CustomLoginRequiredMixin, CustomAuthorizationMixin
from decimal import Decimal
from reservation.ReservationSerializer import (
    ReservationSerializer,
    PlatformSerializer,
    ApartmentSerializer,
    TaxRateSerializer,
    InvoiceSerializer,
    InvoiceWithReservationSerializer,
)
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
)
from rest_framework import permissions as permission
from rest_framework.permissions import IsAdminUser, IsAuthenticated


RESERVATION_URL = "/mini/reservation"
LOGIN_URL = "/login"
PLATFORM_URL = "/mini/platform"
APARTMENT_URL = "/mini/apartment"
TAX_RATE_URL = "/mini/taxrate"


# view of reservation pages
class ResDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Reservation
    success_url = RESERVATION_URL
    template_name = "booking/res_delete.html"
    login_url = LOGIN_URL


class ResUpdateView(UpdateView):
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
        form.initial["user"] = request.user
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
        queryset = self.request.user.reservation.order_by(F("start_date").asc())

        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        name = self.request.GET.get("name")

        if start_date and end_date:
            queryset = queryset.filter(
                start_date__gte=start_date, end_date__lte=end_date
            )

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class ResDetailView(CustomLoginRequiredMixin, DetailView):
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


class PltDetailView(CustomLoginRequiredMixin, DetailView):
    model = Platform
    template_name = "platform/plt_detail.html"
    context_object_name = "plt"
    # login_url = "/login"


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


class PltUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Platform
    template_name = "platform/plt_form.html"
    success_url = PLATFORM_URL
    form_class = PlatformForm
    login_url = LOGIN_URL


class PltDeleteView(CustomLoginRequiredMixin, DeleteView):
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


class AptDetailView(CustomLoginRequiredMixin, DetailView):
    model = Apartment
    template_name = "apartment/apt_detail.html"
    context_object_name = "apt"
    # login_url = LOGIN_URL


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


class AptUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Apartment
    template_name = "apartment/apt_form.html"
    success_url = APARTMENT_URL
    form_class = ApartmentForm
    login_url = LOGIN_URL


class AptDeleteView(CustomLoginRequiredMixin, DeleteView):
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
        # return TaxRate.objects.all()
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


class TaxRateDeleteView(LoginRequiredMixin, DeleteView):
    model = TaxRate
    success_url = TAX_RATE_URL
    template_name = "settings/tax_delete.html"
    login_url = LOGIN_URL


# invoice pages


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "invoice/inv_list.html"
    context_object_name = "invoices"
    login_url = LOGIN_URL

    def get_queryset(self):
        invoices = Invoice.objects.filter(reservation__user=self.request.user)
        return invoices


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
        context["number_of_nights"] = number_of_nights
        context["citytax"] = citytax
        context["vat"] = vat
        context["netto"] = netto

        return context


# invoice as a table

# def get_invoice_context(instance):
#     context = {}
#     context['invoices'] = instance
#     context['reservation'] = instance.reservation
#     return context


class InvoiceDetailedView(DetailView):
    model = Invoice
    template_name = "invoice/inv_detail1.html"
    context_object_name = "invoices"

    def get_template_names(self):
        invoice = self.get_object()
        res_user_id = invoice.reservation.user_id
        user_id = self.request.user.id
        if res_user_id != user_id:
            return ["invoice/404.html"]

        if self.request.user.country == "Poland":
            return ["invoice/inv_detail_pl.html"]
        else:
            return ["invoice/inv_detail1.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = self.get_object()
        res_user_id = invoice.reservation.user_id
        user_id = self.request.user.id
        if res_user_id == user_id:
            invoice = self.object
            reservation = invoice.reservation
            context["invoices"] = invoice
            context["reservation"] = reservation

            return context


class GeneratePdf(View):
    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Invoice, pk=pk)
        if request.user.country == "Poland":
            print("in poland")
            template_name = "invoice/inv_detail_pl_pdf.html"
        else:
            print("in germany")
            template_name = "invoice/inv_detailed1_pdf.html"

        context = get_invoice_context(instance)
        pdf = render_to_pdf(template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "PDF_%s.pdf" % ("Invoice")
            content = "inline; filename= %s" % (filename)
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Page Not Found")


class CityTaxReportView(CustomAuthorizationMixin, View):
    template_name = "reports/city_tax_report.html"

    def get(self, request):
        form = ReportForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            purpose_totals = {}
            grand_total = {
                "total_nights": 0,
                "total_netto": Decimal("0.00"),
                "total_tax": Decimal("0.00"),
                "total_vat": Decimal("0.00"),
                "total_total": Decimal("0.00"),
            }

            for purpose, _ in Reservation.PURPOSE_CHOICES:
                reservations = Reservation.objects.filter(
                    start_date__gte=start_date,
                    end_date__lte=end_date,
                    user=request.user,
                    purpose=purpose,
                )

                total_nights = sum((res.number_of_nights() for res in reservations))
                total_netto = sum((res.calculate_netto() for res in reservations))
                total_tax = sum((res.calculate_citytax() for res in reservations))
                total_vat = sum((res.calculate_vat() for res in reservations))
                total_total = total_netto + total_tax + total_vat

                purpose_totals[purpose] = {
                    "total_nights": total_nights,
                    "total_netto": total_netto,
                    "total_tax": total_tax,
                    "total_vat": total_vat,
                    "total_total": total_total,
                }

                grand_total["total_nights"] += total_nights
                grand_total["total_netto"] += total_netto
                grand_total["total_tax"] += total_tax
                grand_total["total_vat"] += total_vat
                grand_total["total_total"] += total_total

            vat_rate = request.user.taxrates.latest("start_date").vat_rate
            city_tax_rate = request.user.taxrates.latest("start_date").citytax_rate

            print("vat rate: ", vat_rate)

            context = {
                "form": form,
                "vat_rate": vat_rate,
                "city_tax_rate": city_tax_rate,
                "purpose_totals": purpose_totals,
                "grand_total": grand_total,
            }

            return render(request, self.template_name, context)
        else:
            # Handle form validation errors
            context = {"form": form}
            return render(request, self.template_name, context)


# api's
class ReservationAPIView(ListCreateAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)


class ReservationDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ApartmentAPIView(ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ApartmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class PlatformAPIView(ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class PlatformDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class TaxRateAPIView(ListAPIView):
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class TaxRateDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class InvoiceAPIView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class InvoiceDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceWithReservationSerializer
    permission_classes = (IsOwnerOrReadOnly,)
