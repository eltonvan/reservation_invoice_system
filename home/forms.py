from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "input-group-text"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input-group-text"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input-group-text"}))
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "name",
            "last_name",
            "street",
            "house_number",
            "zip_code",
            "city",
            "birthday",
            "email",
            "country",
            "phone_number",
            "tax_number",
            "bank_account",
        )


        widgets = {
            "name": forms.TextInput(attrs={"class": "input-group-text"}),
            "last_name": forms.TextInput(attrs={"class": "input-group-text"}),
            "street": forms.TextInput(attrs={"class": "input-group-text"}),
            "house_number": forms.TextInput(attrs={"class": "input-group-text"}),
            "city": forms.TextInput(attrs={"class": "input-group-text"}),
            "zip_code": forms.TextInput(attrs={"class": "input-group-text"}),
            "birthday": forms.DateInput(attrs={"class": "input-group-text"}),
            "email": forms.EmailInput(attrs={"class": "input-group-text"}),
            "country": forms.TextInput(attrs={"class": "input-group-text"}),
            "phone_number": forms.TextInput(attrs={"class": "input-group-text"}),
            "tax_number": forms.TextInput(attrs={"class": "input-group-text"}),
            "bank_account": forms.TextInput(attrs={"class": "input-group-text"}),
        }

        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            self.fields["name"].widget.attrs["placeholder"] = "Name"
            self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
            self.fields["street"].widget.attrs["placeholder"] = "Street"
            self.fields["house_number"].widget.attrs["placeholder"] = "House Number"
            self.fields["city"].widget.attrs["placeholder"] = "City"
            self.fields["zip_code"].widget.attrs["placeholder"] = "Zip Code"
            self.fields["birthday"].widget.attrs["placeholder"] = "Birthday"
            self.fields["email"].widget.attrs["placeholder"] = "Email"
            self.fields["country"].widget.attrs["placeholder"] = "Country"
            self.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
            self.fields["tax_number"].widget.attrs["placeholder"] = "Tax Number"
            self.fields["bank_account"].widget.attrs["placeholder"] = "Bank Account"
