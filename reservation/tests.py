from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import TaxRate, Platform, Apartment, Reservation, Invoice

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
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(pk=1, username='testuser', password='12345', email = 'sss@fff.com')
        cls.platform = Platform.objects.create(user=cls.user, name="Test Platform", address="Test Address")
        cls.apartment = Apartment.objects.create(user=cls.user, name="Test Apartment", address="Test Address", date_contract=date.today())
        cls.reservation = Reservation.objects.create(
            start_date=date(2023, 10, 10),
            end_date=date(2023, 10, 12),
            name='Test Reservation',
            t_sum=Decimal('100.00'),
            commission=Decimal('10.00'),
            number_of_guests=2,
            lname='Test Lastname',
            company='Test Company',
            address='Test Address',
            user=cls.user,
            platform=cls.platform,
            apartment=cls.apartment,
        )

    def test_reservation_detail_view(self):

       
        self.assertEqual(self.reservation.user, self.user)



    def test_reservation_createview(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('reservation.new'), {
            'start_date': date(2023, 10, 10),
            'end_date': date(2023, 10, 12),
            'name': 'Test Reservation',
            't_sum': Decimal('100.00'),
            'commission': Decimal('10.00'),
            'number_of_guests': 2,
            'lname': 'Test Lastname',
            'company': 'Test Company',
            'address': 'Test Address',
            'user': self.user,
            'platform': self.platform,
            'apartment': self.apartment,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Reservation')


    def test_rev_createview(self):
        response = self.client.post(reverse('reservation.new'), {
            'start_date': date(2023, 10, 10),
            'end_date': date(2023, 10, 12),
            'name': 'Test Reservation',
            't_sum': Decimal('100.00'),
            'commission': Decimal('10.00'),
            'number_of_guests': 2,
            'lname': 'Test Lastname',
            'company': 'Test Company',
            'address': 'Test Address',
            'user': self.user,
            'platform': self.platform,
            'apartment': self.apartment,
        })
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(Reservation.object.last().name, 'Test Reservation')

