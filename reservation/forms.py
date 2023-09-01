from django import forms
from django.core.exceptions import ValidationError
from home import models
from .models import Reservation, User, Platform, Apartment, TaxRate
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django import forms
from django.forms.widgets import DateInput




    

class DateInput(forms.DateInput):
    input_type = "date"
    input_formats = ['%d-%m-%Y']


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


    class Meta:
        model = TaxRate
        fields = ["start_date", "vat_rate", "citytax_rate", "tax_zone"]
        widgets = {
            "vat_rate": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "citytax_rate": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "tax_zone": forms.TextInput(attrs={"class": "form-control mb-5"}),
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
        if user and not self.instance.user:
            self.fields["user"].initial = user
            self.fields['user'].widget = forms.HiddenInput()
            

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
            "number_of_guests",
            "apartment",
            "platform",
            "company",
            "email",
            "nationality",
            "comment",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "lname": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "t_sum": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "company": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "address": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "email": forms.EmailInput(attrs={"class": "form-control mb-5"}),
            "number_of_guests": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "purpose": forms.Select(attrs={"class": "form-control mb-5"}),
            "commission": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "rech_num": forms.TextInput(attrs={"class": "form-control mb-5"}),
            "link": forms.URLInput(attrs={"class": "form-control mb-5"}),
            "user": forms.Select(attrs={"class": "form-control mb-5"}),
            "apartment": forms.Select(attrs={"class": "form-control mb-5"}),
            "platform": forms.Select(attrs={"class": "form-control mb-5"}),
            "comment": forms.Textarea(attrs={"class": "form-control mb-5"}),
        }
