from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import TaxRate, Platform, Apartment, Reservation, CustomUser
from .forms import ReservationForm, PlatformForm, ApartmentForm, TaxRateForm, ReportForm
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# user authentication

# model creation and retrieval

# view rendering


class ViewTests(TestCase):
    def test_reservation_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse('reservation.list'))
        self.assertEqual(response.status_code, 200)

    def test_platform_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse('platform.list'))
        self.assertEqual(response.status_code, 200)

    def test_apartment_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse('apartment.list'))
        self.assertEqual(response.status_code, 200)

    def test_tax_rate_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse('taxrate.list'))
        self.assertEqual(response.status_code, 200)

    def test_invoice_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse('invoice.list'))
        self.assertEqual(response.status_code, 200)


class ReservationDetailViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", id=1)
        self.platform = Platform.objects.create(user=self.user, name="Test Platform", address="Test Address")
        self.apartment = Apartment.objects.create(user=self.user, name="Test Apartment", address="Test Address", date_contract=date.today())
        self.reservation = Reservation.objects.create(
            start_date='2023-10-10',
            end_date='2023-10-12',
            name='Test Reservation',
            t_sum=Decimal('100.00'),
            commission=Decimal('10.00'),
            number_of_guests=2,
            lname='Test Lastname',
            company='Test Company',
            address='Test Address',
            user=self.user,
            platform=self.platform,
            apartment=self.apartment
        )

    def test_reservation_detail_view(self):
        response = self.client.get(reverse('reservation.detail', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Reservation')



# url routing

# crus operations




#custom template tags

# error handeling


# performance

# security


