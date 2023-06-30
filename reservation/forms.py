from django import forms
from django.core.exceptions import ValidationError

from home import models
from .models import Reservation, User




class DateInput(forms.DateInput):
    input_type = 'date'
 
class ReservationForm(forms.ModelForm):

  
    start_date = forms.DateField(widget=DateInput(attrs={'class': 'form-control my-5'}))
    end_date = forms.DateField(widget=DateInput(attrs={'class': 'form-control my-5'}))
    class Meta:
        model = Reservation
        fields = ['start_date','end_date','name', 'lname',  't_sum', 'user']
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control mb-5'}),
            'lname': forms.TextInput(attrs={'class': 'form-control mb-5'}),
            't_sum': forms.NumberInput(attrs={'class': 'form-control mb-5'}),
        #     'apartment': forms.Select(attrs={'class': 'form-control mb-5'}),
        #     'platform': forms.Select(attrs={'class': 'form-control mb-5'}),
        }
        #labels = {'start_date': 'Check-in', 'end_date': 'Checkout', 'num_guests': 'Number of Guests', 'fname': 'First Name', 'lname': 'Last Name', 'email': 'Email', 'purpose': 'Purpose', 'company': 'Company', 't_sum': 'Total Sum', 'commission': 'Commission', 'rech_num': 'Rechnung Number', 'link_reservation': 'Link Reservation', 'guest_document': 'Guest Document', 'apartment': 'Apartment', 'platform': 'Platform'}


