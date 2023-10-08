from django import forms
from django.core.exceptions import ValidationError
from home import models
from home.models import CustomUser
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


    class Meta:
        model = TaxRate
        fields = ["start_date", "vat_rate", "citytax_rate", "tax_zone"]
        widgets = {
            "vat_rate": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "citytax_rate": forms.NumberInput(attrs={"class": "form-control mb-5"}),
            "tax_zone": forms.TextInput(attrs={"class": "form-control mb-5"}),
        }




class ReservationForm(forms.ModelForm):
    
    start_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    end_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    nationality = CountryField().formfield(
        initial="", widget=CountrySelectWidget(attrs={"class": "form-control"})
    )
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.HiddenInput(),
        required=False  
    )


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
            "user"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "lname": forms.TextInput(attrs={"class": "form-control"}),
            "t_sum": forms.NumberInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "number_of_guests": forms.NumberInput(attrs={"class": "form-control"}),
            "purpose": forms.Select(attrs={"class": "form-control"}),
            "commission": forms.NumberInput(attrs={"class": "form-control"}),
            "rech_num": forms.TextInput(attrs={"class": "form-control"}),
            "link": forms.URLInput(attrs={"class": "form-control"}),
            "apartment": forms.Select(attrs={"class": "form-control"}),
            "platform": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("in form: ", user)
        if user:

            user_apartments = Apartment.objects.filter(user=user)
            self.fields["apartment"].queryset = user_apartments

            user_platforms = Platform.objects.filter(user=user)
            self.fields["platform"].queryset = user_platforms
        
        default_country = 'DE'
        if not self.instance.nationality:
            self.initial['nationality'] = default_country
  


        