from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('name', 'last_name', 'street', 'house_number', 'zip_code', 'birthday', 'email', 'country', 'phone_number', 'tax_number', 'bank_account')
