from django.test import TestCase
from django.urls import reverse, reverse_lazy
from datetime import date
from .models import TaxRate, Platform, Apartment, Reservation, Invoice
from home.models import CustomUser
from .forms import ReservationForm, PlatformForm, ApartmentForm, TaxRateForm, ReportForm
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework import status


class BaseTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            pk=1, username="testuser", password="123Testing", email="sss@fff.com"
        )

        cls.user2 = get_user_model().objects.create_user(
            pk=2, username="testuser2", password="123Testing", email="sss@testing.com"
        )
        cls.platform = Platform.objects.create(
            user=cls.user, name="Test Platform", address="Test Address"
        )
        cls.apartment = Apartment.objects.create(
            user=cls.user,
            name="Test Apartment",
            address="Test Address",
            date_contract=date.today(),
        )
        cls.reservation = Reservation.objects.create(
            start_date=date(2023, 10, 10),
            end_date=date(2023, 10, 12),
            name="Test Reservation",
            t_sum=Decimal("100.00"),
            commission=Decimal("10.00"),
            number_of_guests=2,
            lname="Test Lastname",
            company="Test Company",
            address="Test Address",
            user=cls.user,
            platform=cls.platform,
            apartment=cls.apartment,
        )

        cls.taxrate = TaxRate.objects.create(
            user=cls.user,
            start_date=date.today(),
            vat_rate=Decimal("10.00"),
            citytax_rate=Decimal("10.00"),
            tax_zone="Test Tax Zone",
        )

        cls.invoice = Invoice.objects.create(
            name="Test Invoice",
            invoice_netto=Decimal("100.00"),
            invoice_vat=Decimal("10.00"),
            invoice_citytax=Decimal("10.00"),
            invoice_number_of_nights=2,
            reservation=cls.reservation,
        )


class ReservationDetailViewTest(BaseTestSetup, TestCase):
    def test_reservation_detail_view(self):
        self.assertEqual(self.reservation.user, self.user)

    def test_reservation_createview(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("reservation.new"),
            {
                "start_date": date(2023, 10, 10),
                "end_date": date(2023, 10, 12),
                "name": "Test Reservation",
                "t_sum": Decimal("100.00"),
                "commission": Decimal("10.00"),
                "number_of_guests": 2,
                "lname": "Test Lastname",
                "company": "Test Company",
                "address": "Test Address",
                "user": self.user,
                "platform": self.platform.pk,
                "apartment": self.apartment.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Test Reservation",
        )

    # def test_rev_createview(self):
    #     self.client.force_login(self.user2)
    #     response = self.client.post(
    #         reverse("reservation.new"),
    #         {
    #             "start_date": date(2023, 10, 10),
    #             "end_date": date(2023, 10, 12),
    #             "name": "Test Reservation",
    #             "t_sum": Decimal("100.00"),
    #             "commission": Decimal("10.00"),
    #             "number_of_guests": 2,
    #             "lname": "Test Lastname",
    #             "company": "Test Company",
    #             "address": "Test Address",
    #             "user": self.user,
    #             "platform": self.platform,
    #             "apartment": self.apartment,
    #         },
    #     )
    #     self.assertEqual(response.status_code, 302)

    #     self.assertEqual(Reservation.object.last().name, "Test Reservation")


class TestReservationModel(BaseTestSetup, TestCase):
    def test_reservation_model_str(self):
        self.assertEqual(str(self.reservation.name), "Test Reservation")


class TestReservationViews(BaseTestSetup, TestCase):
    def test_reservation_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reservation.list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Reservation")
        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "booking/res_list.html")
        # check that the user is logged in
        self.client.login(username="testuser", password="123Testing")
        response = self.client.get(reverse("reservation.list"))
        self.assertTrue(response.context["user"].is_authenticated)

        # login user 2
        self.client.force_login(self.user2)
        response = self.client.get(reverse("reservation.list"))

        # Check if user2 doesn't see objects associated with user
        self.assertNotContains(response, "Test Reservation")
        # check that there are no reservations at all
        reservations = Reservation.objects.filter(user=self.user2)
        self.assertEqual(reservations.count(), 0)

        self.assertEqual(response.status_code, 200)

    def Test_reservation_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("reservation.detail", kwargs={"pk": self.reservation.pk}),
            follow=True,
        )
        # Check that the rendered context contains the reservation from the database.
        self.assertContains(response, self.reservation.name)

        self.assertEqual(response.status_code, 200)

    def Test_reservation_detail_view_wrong_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse("reservation.detail", kwargs={"pk": self.reservation.pk}),
            follow=True,
        )
        # Check that the redirect url is correct
        self.assertEqual(response.status_code, 404)

    def Test_reservation_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("reservation.new"), follow=True)
        self.assertEqual(response.status_code, 200)
        # Check that the form is rendered correctly
        self.assertContains(response, "form")
        # check the user is redirected to page after form submission
        form = response.context["form"]
        self.assertEqual(form.initial["user"], self.user)

        form_data = {
            "start_date": date(2023, 10, 10),
            "end_date": date(2023, 10, 12),
            "name": "Test Reservation4te",
            "t_sum": Decimal("100.00"),
            "commission": Decimal("10.00"),
            "number_of_guests": 2,
            "lname": "Test Lastname",
            "company": "Test Company",
            "address": "Test Address",
            "user": self.user,
            "platform": self.platform.pk,
            "apartment": self.apartment.pk,
        }
        response = self.client.post(
            reverse("reservation.new"), data=form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)  # Or 302 if redirected
        self.assertRedirects(response, reverse("reservation.list"))  # Check redirect
        # check that the user is correctly associated with the location in the database
        print(Reservation.objects.first())
        reservation = Reservation.objects.get(name="Test Reservation4")
        print("reservation object", reservation)
        self.assertEqual(reservation.user, self.reservation.user)

    def reservation_delete_view_test(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("reservation.delete", kwargs={"pk": self.reservation.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Reservation")
        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "booking/res_delete.html")
        # check that the user is logged in
        self.client.login(username="testuser", password="123Testing")
        response = self.client.get(
            reverse("reservation.delete", kwargs={"pk": self.reservation.pk}),
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

        # login user 2
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse("reservation.delete", kwargs={"pk": self.reservation.pk}),
            follow=True,
        )

        # Check if user2 is redirected to 404
        self.assertEqual(response.status_code, 404)
        # check that there are no reservations at all
        reservations = Reservation.objects.filter(user=self.user2)
        self.assertEqual(reservations.count(), 0)


class ViewTests(TestCase):
    def test_reservation_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse("reservation.list"))
        self.assertEqual(response.status_code, 200)

    def test_platform_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse("platform.list"))
        self.assertEqual(response.status_code, 200)

    def test_apartment_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse("apartment.list"))
        self.assertEqual(response.status_code, 200)

    def test_tax_rate_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse("taxrate.list"))
        self.assertEqual(response.status_code, 200)

    def test_invoice_list_view(self):
        user = CustomUser.objects.create(name="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse("invoice.list"))
        self.assertEqual(response.status_code, 200)


class TestApartmentsViews(BaseTestSetup, TestCase):
    def test_apartment_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("apartment.list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Apartment")
        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "apartment/apt_list.html")
        # check that the user is logged in
        self.client.login(username="testuser", password="123Testing")
        response = self.client.get(reverse("apartment.list"))
        self.assertTrue(response.context["user"].is_authenticated)

        # login user 2
        self.client.force_login(self.user2)
        response = self.client.get(reverse("apartment.list"))

        # Check if user2 doesn't see objects associated with user
        self.assertNotContains(response, "Test Apartment")
        # check that there are no reservations at all
        apartments = Apartment.objects.filter(user=self.user2)
        self.assertEqual(apartments.count(), 0)

        self.assertEqual(response.status_code, 200)

    def Test_apartment_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("apartment.detail", kwargs={"pk": self.apartment.pk}),
            follow=True,
        )
        # Check that the rendered context contains the reservation from the database.
        self.assertContains(response, self.apartment.name)

        self.assertEqual(response.status_code, 200)

    def Test_apartment_detail_view_wrong_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse("apartment.detail", kwargs={"pk": self.apartment.pk}),
            follow=True,
        )
        # Check that the redirect url is correct
        self.assertEqual(response.status_code, 404)

    def Test_apartment_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("apartment.new"), follow=True)
        self.assertEqual(response.status_code, 200)
        # Check that the form is rendered correctly
        self.assertContains(response, "form")
        # check the user is redirected to page after form submission
        form = response.context["form"]
        self.assertEqual(form.initial["user"], self.user)

        form_data = {
            "name": "Test Apartment",
            "address": "Test Address",
            "date_contract": date.today(),
            "user": self.user,
        }


class TestPlatformViews(BaseTestSetup, TestCase):
    def test_platform_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("platform.list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Platform")
        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "platform/plt_list.html")
        # check that the user is logged in
        self.client.login(username="testuser", password="123Testing")
        response = self.client.get(reverse("platform.list"))
        self.assertTrue(response.context["user"].is_authenticated)

        # login user 2
        self.client.force_login(self.user2)
        response = self.client.get(reverse("platform.list"))

        # Check if user2 doesn't see objects associated with user
        self.assertNotContains(response, "Test Platform")
        # check that there are no reservations at all
        platforms = Platform.objects.filter(user=self.user2)
        self.assertEqual(platforms.count(), 0)

        self.assertEqual(response.status_code, 200)

    def Test_platform_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("platform.detail", kwargs={"pk": self.platform.pk}),
            follow=True,
        )
        # Check that the rendered context contains the reservation from the database.
        self.assertContains(response, self.platform.name)

        self.assertEqual(response.status_code, 200)

    def Test_platform_detail_view_wrong_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse("platform.detail", kwargs={"pk": self.platform.pk}),
            follow=True,
        )
        # Check that the redirect url is correct
        self.assertEqual(response.status_code, 404)

    def Test_platform_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("platform.new"), follow=True)
        self.assertEqual(response.status_code, 200)
        # Check that the form is rendered correctly
        self.assertContains(response, "form")
        # check the user is redirected to page after form submission
        form = response.context["form"]
        self.assertEqual(form.initial["user"], self.user)

        form_data = {
            "name": "Test Platform",
            "address": "Test Address",
            "user": self.user,
        }

        response = self.client.post(reverse("platform.new"), data=form)
        self.assertEqual(response.status_code, 302)


class TestTaxrateViews(BaseTestSetup, TestCase):
    def test_taxrate_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxrate.list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Tax Zone")
        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "settings/tax_list.html")
        # check that the user is logged in
        self.client.login(username="testuser", password="123Testing")
        response = self.client.get(reverse("taxrate.list"))
        self.assertTrue(response.context["user"].is_authenticated)

        # login user 2
        self.client.force_login(self.user2)
        response = self.client.get(reverse("taxrate.list"))

        # Check if user2 doesn't see objects associated with user
        self.assertNotContains(response, "Test Taxrate")
        # check that there are no reservations at all
        taxrates = TaxRate.objects.filter(user=self.user2)
        self.assertEqual(taxrates.count(), 0)

        self.assertEqual(response.status_code, 200)

    def Test_taxrate_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxrate.detail", kwargs={"pk": self.taxrate.pk}),
            follow=True,
        )
        # Check that the rendered context contains the reservation from the database.
        self.assertContains(response, self.taxrate.name)

        self.assertEqual(response.status_code, 200)

    def Test_taxrate_detail_view_wrong_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse("taxrate.detail", kwargs={"pk": self.taxrate.pk}),
            follow=True,
        )
        # Check that the redirect url is correct
        self.assertEqual(response.status_code, 404)

    def Test_taxrate_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxrate.new"), follow=True)
        self.assertEqual(response.status_code, 200)
        # Check that the form is rendered correctly
        self.assertContains(response, "form")
        # check the user is redirected to page after form submission
        form = response.context["form"]
        self.assertEqual(form.initial["user"], self.user)

        form_data = {
            "name": "Test Taxrate",
            "address": "Test Address",
            "user": self.user,
        }

        response = self.client.post(reverse("taxrate.new"), data=form)
        self.assertEqual(response.status_code, 302)


class InvoiceTestsViews(BaseTestSetup, TestCase):
    def test_invoice_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("invoice.list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Invoice")
        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "invoice/inv_list.html")
        # check that the user is logged in
        self.client.login(username="testuser", password="123Testing")
        response = self.client.get(reverse("invoice.list"))
        self.assertTrue(response.context["user"].is_authenticated)

        # login user 2
        self.client.force_login(self.user2)
        response = self.client.get(reverse("invoice.list"))

        # Check if user2 doesn't see objects associated with user
        self.assertNotContains(response, "Test Invoice")
        # check that there are no reservations at all
        invoices = Invoice.objects.filter(user=self.user2)
        self.assertEqual(invoices.count(), 0)

        self.assertEqual(response.status_code, 200)

    def Test_invoice_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("invoice.detail", kwargs={"pk": self.invoice.pk}),
            follow=True,
        )
        # Check that the rendered context contains the reservation from the database.
        self.assertContains(response, self.invoice.name)

        self.assertEqual(response.status_code, 200)

    def Test_invoice_detail_view_wrong_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse("invoice.detail", kwargs={"pk": self.invoice.pk}),
            follow=True,
        )
        # Check that the redirect url is correct
        self.assertEqual(response.status_code, 404)

    def Test_invoice_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("invoice.new"), follow=True)
        self.assertEqual(response.status_code, 200)
        # Check that the form is rendered correctly
        self.assertContains(response, "form")
        # check the user is redirected to page after form submission
        form = response.context["form"]
        self.assertEqual(form.initial["user"], self.user)

        form_data = {
            "name": "Test Invoice",
            "address": "Test Address",
            "date": date.today(),
            "number": "Test Number",
            "tax_rate": self.taxrate.pk,
            "platform": self.platform.pk,
            "apartment": self.apartment.pk,
            "reservation": self.reservation.pk,
            "user": self.user,
        }

        response = self.client.post(reverse("invoice.new"), data=form)
        self.assertEqual(response.status_code, 302)


# api tests


class TestReservationApiViews(BaseTestSetup, APITestCase):
    def test_reservation_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("api.reservation.list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Reservation")
        # Check that the rendered context contains the restaurant from the database.
        self.assertTemplateUsed(response, "booking/res_list.html")
        # check that the user is logged in
        self.client.login(username="testuser", password="123Testing")
        response = self.client.get(reverse("api.reservation.list"))
        self.assertTrue(response.context["user"].is_authenticated)

        # login user 2
        self.client.force_login(self.user2)
        response = self.client.get(reverse("api.reservation.list"))

        # Check if user2 doesn't see objects associated with user
        self.assertNotContains(response, "Test Reservation")
        # check that there are no reservations at all
        reservations = Reservation.objects.filter(user=self.user2)
        self.assertEqual(reservations.count(), 0)

        self.assertEqual(response.status_code, 200)

    def Test_reservation_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("api.reservation.detail", kwargs={"pk": self.reservation.pk}),
            follow=True,
        )
        # Check that the rendered context contains the reservation from the database.
        self.assertContains(response, self.reservation.name)

        self.assertEqual(response.status_code, 200)

    def Test_reservation_detail_view_wrong_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse("api.reservation.detail", kwargs={"pk": self.reservation.pk}),
            follow=True,
        )
        # Check that the redirect url is correct
        self.assertEqual(response.status_code, 404)

    def Test_reservation_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("api.reservation.new"), follow=True)
        self.assertEqual(response.status_code, 200)
        # Check that the form is rendered correctly
        self.assertContains(response, "form")
        # check the user is redirected to page after form submission
        form = response.context["form"]
        self.assertEqual(form.initial["user"], self.user)

        form_data = {
            "start_date": date(2023, 10, 10),
            "end_date": date(2023, 10, 12),
            "name": "Test Reservation",
            "t_sum": Decimal("100.00"),
            "commission": Decimal("10.00"),
            "number_of_guests": 2,
            "lname": "Test Lastname",
            "company": "Test Company",
            "user": self.user,
            "platform": self.platform.pk,
            "apartment": self.apartment.pk,
        }

        response = self.client.post(reverse("api.reservation.new"), data=form_data)
        self.assertEqual(response.status_code, 201)
