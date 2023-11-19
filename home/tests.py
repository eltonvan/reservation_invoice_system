from django.test import TestCase
from django.urls import reverse, resolve
from datetime import date
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = CustomUser.objects.create_user(
            is_superuser=True,
            username="testuser1",
            password="abc123",
            email="user1@testsite.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            is_staff=True,
        )
        testuser1.save()

        testuser2 = CustomUser.objects.create_user(
            username="testuser2",
            password="abc123",
            email="user2@testsite.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            is_staff=True,
        )
        testuser2.save()

        def test_users_content(self):
            user = CustomUser.objects.get(id=1)
            expected_object_name = f"{user.username}"
            self.assertEquals(expected_object_name, "testuser1")
            self.assertEquals(user.email, "user1@testsite.com")
            self.assertEquals(user.first_name, "Test")
            self.assertEquals(user.last_name, "User")
            self.assertEquals(user.phone_number, "1234567890")
            self.assertEquals(user.city, "Test City")
            self.assertEquals(user.zip_code, "12345")
            self.assertEquals(user.country, "Test Country")
            self.assertEquals(user.is_staff, True)

        def test_users_list_view(self):
            self.client.login(username="testuser1", password="abc123")
            response = self.client.get(reverse("user_list"))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "testuser1")
            self.assertTemplateUsed(response, "home/user_list.html")


class CustomUserCreationFormTest(TestCase):
    def test_custom_user_creation_form_valid_data(self):
        form = CustomUserCreationForm(
            data={
                "username": "testuser1",
                "password1": "abc123Testing",
                "password2": "abc123Testing",
                "name": "Test",
                "house_number": "123",
                "tax_number": "1234567890",
                "bank_account": "1234567890",
                "birthday": "1990-01-01",
                "email": "tester@testsite.com",
                "country": "Test Country",
                "zip_code": "12345",
                "city": "Test City",
                "phone_number": "1234567890",
                "last_name": "User",
                "name": "Test",
            }
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        user = form.save()
        self.assertEqual(user.username, "testuser1")
        self.assertEqual(user.email, "tester@testsite.com")
        self.assertEqual(user.country, "Test Country")
        self.assertEqual(user.zip_code, "12345")
        self.assertEqual(user.city, "Test City")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.name, "Test")


class CustomUserUpdateFormTest(TestCase):
    pass


class CustomUserApiTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create_user(
            is_superuser=False,
            username="testuser1",
            password="abc123Testing",
            email="user1@testsite.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            is_staff=True,
        )
        cls.user2 = CustomUser.objects.create_user(
            username="testuser2",
            password="abc123Testing",
            email="user2@testsite.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            is_staff=False,
        )
        cls.admin_user = CustomUser.objects.create_superuser(
            is_superuser=True,
            username="testuser",
            password="abc123testing",
            email="user@testsite.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            city="Test City",
            zip_code="12345",
            country="Test Country",
            is_staff=True,
        )
        cls.url_list = reverse("user-list")
        cls.url_detail = reverse("user-detail", args=[cls.user.pk])
        cls.url_create = reverse("user-create")

    def test_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_unauthenticated(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_unauthenticated(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "username": "testuser3",
            "password": "abc123Testing",
            "email": "user3@testsite.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
            "city": "Test City",
            "zip_code": "12345",
            "country": "Test Country",
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(
            response.data.get("id")
        )  # Ensure user ID is present in the response

    # def test_modify_user(self):
    #     self.client.force_authenticate(user=self.user)
    #     data = {
    #         "username": "testuser4",
    #         "password": "abc123Testing",
    #         "email": "user4@testsite.com",
    #         "first_name": "Test",
    #         "last_name": "User",
    #         "phone_number": "1234567890",
    #         "city": "Test City",
    #         "zip_code": "12345",
    #         "country": "Test Country1",
    #     }
    #     response = self.client.patch(self.url_detail, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
