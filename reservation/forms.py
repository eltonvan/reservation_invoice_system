from django import forms
from django.core.exceptions import ValidationError
from home import models
from .models import Reservation, User, Platform, Apartment, TaxRate
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class DateInput(forms.DateInput):
    input_type = "date"


class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ["name", "address", "kundennummer", "tel", "login", "url"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "address": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "kundennummer": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "tel": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "login": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "url": forms.TextInput(attrs={"class": "form-control mb-5"}),
        }


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ["name", "address", "date_contract"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "address": forms.TextInput(attrs={"class": "form-control mb-5"}),
        }

    date_contract = forms.DateField(
        widget=DateInput(attrs={"class": "form-control my-5"})
    )


class TaxRateForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(attrs={"class": "form-control my-5"}))

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(TaxRateForm, self).__init__(*args, **kwargs)
    #     if user:
    #         self.fields['user'].initial = user
    class Meta:
        model = TaxRate
        fields = ["start_date", "vat_rate", "citytax_rate"]
        widgets = {
            "vat_rate": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "citytax_rate": forms.NumberInput(attrs={"class": "form-control mb-5"}),
        }


class ReservationForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(attrs={"class": "form-control my-5"}))
    end_date = forms.DateField(widget=DateInput(attrs={"class": "form-control my-5"}))
    nationality = CountryField().formfield(
        initial="", widget=CountrySelectWidget(attrs={"class": "form-control mb-5"})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ReservationForm, self).__init__(*args, **kwargs)

        default_country = 'DE'  # Replace 'US' with the desired default country code

        if not self.instance.nationality:
            self.initial['nationality'] = default_country
        if user:
            self.fields["user"].initial = user

    class Meta:
        model = Reservation
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
            "user",
            "apartment",
            "platform",
            "company",
            "email",
            "nationality",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "lname": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "t_sum": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "company": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "address": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "email": forms.EmailInput(attrs={"class": "form-control mb-5"}),
            #'nationality': CountrySelectWidget(attrs={'class': 'form-control mb-5'}),
            "purpose": forms.Select(attrs={"class": "form-control mb-5"}),
            "commission": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "rech_num": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "link": forms.URLInput(attrs={"class": "form-control mb-5"}),
            "user": forms.Select(attrs={"class": "form-control mb-5"}),
            "apartment": forms.Select(attrs={"class": "form-control mb-5"}),
            "platform": forms.Select(attrs={"class": "form-control mb-5"}),
        }
        # labels = {'start_date': 'Check-in', 'end_date': 'Checkout', 'num_guests': 'Number of Guests', 'fname': 'First Name', 'lname': 'Last Name', 'email': 'Email', 'purpose': 'Purpose', 'company': 'Company', 't_sum': 'Total Sum', 'commission': 'Commission', 'rech_num': 'Rechnung Number', 'link_reservation': 'Link Reservation', 'guest_document': 'Guest Document', 'apartment': 'Apartment', 'platform': 'Platform'}
