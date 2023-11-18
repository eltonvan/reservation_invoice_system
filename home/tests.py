from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import CustomUser
from .forms import CustomUserCreationForm
from decimal import Decimal
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.urls import resolve



class UserCreationTest(TestCase):
    def test_user_creation(self):
        user_data = {
            'name': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example5s5.com',
            'last_name': 'User',
            'street': 'Test Street',
            'house_number': '1',
            'city': 'Test City',
            'zip_code': '12345',
            'birthday': '1990-01-01',
            'company': 'Test Company',
            'country': 'Test Country',
            'phone_number': '0123456789',
            'tax_number': '1234567890',
            'bank_account': '1234567890',
        }

        # Ensure the user doesn't exist 
        self.assertIsNone(CustomUser.objects.filter(username=user_data['name']).first())

        # Create a new user
        response = self.client.post(reverse('signup'), data=user_data, follow=False)

        # Check if the user was created
        self.assertRedirects(response, reverse('reservation.list'), fetch_redirect_response=False)

        #self.assertEqual(response.status_code, 302)

        # Get the URL name from the response context
        resolved_url_name = resolve(response.request['PATH_INFO']).url_name
        self.assertEqual(resolved_url_name, 'reservation.list')

        # Check if the user now exists
        created_user = CustomUser.objects.get(username=user_data['name'])
        self.assertIsNotNone(created_user)

        # Check if the user can log in 
        login_success = self.client.login(username=user_data['name'], password=user_data['password'])
        self.assertTrue(login_success)



# user permissions

class UserPermissionTest(TestCase):
    def setUp(self):
        # Create a test user with no special permissions
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email = 'testuser@website.com',
            
        )

        # Create a user with the required permission
        self.user_with_permission = get_user_model().objects.create_user(
            username='user_with_permission',
            password='testpassword'
        )
        self.user_with_permission.user_permissions.add(
            Permission.objects.get(codename='can_access_restricted_view')
        )

    def test_restricted_view_permission(self):
        # Test access to the restricted view by a user without permission
        response = self.client.get(reverse('authorized'))
        self.assertEqual(response.status_code, 403)  # HTTP 403 Forbidden

        # Test access to the restricted view by a user with permission
        self.client.force_login(self.user_with_permission)
        response = self.client.get(reverse('authorized'))
        self.assertEqual(response.status_code, 200)  # HTTP 200 OK
