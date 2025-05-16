from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import CompanyManager
from .factories import (
    UserFactory,
    CompanyFactory,
    CompanyOfficeFactory,
    CompanyManagerFactory,
    CountryFactory,
    CityFactory,
)


class CompanyAPITests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create test data
        self.company = CompanyFactory()
        self.country = CountryFactory()
        self.city = CityFactory(country=self.country)
        self.office = CompanyOfficeFactory(
            company=self.company, country=self.country, city=self.city
        )
        self.manager_obj = CompanyManagerFactory(company=self.company)
        self.manager = self.manager_obj.manager

    def test_retrieve_company(self):
        """Test retrieving a specific company"""
        url = reverse("company-retrieve-update", args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.company.name)
        self.assertEqual(response.data["about"], self.company.about)
        self.assertEqual(len(response.data["offices"]), 1)

    def test_manager_updating_company(self):
        """Test updating a company"""
        self.client.force_authenticate(user=self.manager)
        url = reverse("company-retrieve-update", args=[self.company.id])
        data = {
            "name": "Updated Company Name",
            "about": self.company.about,
            "number_of_employees": self.company.number_of_employees,
            "website": "https://updated-website.com",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, data["name"])
        self.assertEqual(self.company.about, data["about"])

    def test_unauthorized_user_updating_company(self):
        """Test updating a company"""
        self.client.force_authenticate(user=self.user)
        url = reverse("company-retrieve-update", args=[self.company.id])
        data = {
            "name": "Updated Company Name",
            "about": "Updated about",
            "website": "https://updated-website.com",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.company.refresh_from_db()
        self.assertNotEqual(self.company.name, data["name"])
        self.assertNotEqual(self.company.about, data["about"])
        self.assertNotEqual(self.company.website, data["website"])


class CompanyManagerAPITests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create test data
        self.company = CompanyFactory()
        self.manager = CompanyManagerFactory(company=self.company)

    def test_list_managers(self):
        """Test retrieving a list of company managers"""
        url = reverse("company-managers-list-create", args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_managers_by_company(self):
        """Test filtering managers by company"""
        # Create another company and manager
        other_company = CompanyFactory()
        CompanyManagerFactory(company=other_company)

        url = reverse("company-managers-list-create", args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.manager.id)

    def test_create_manager(self):
        """Test creating a new company manager"""
        new_user = UserFactory()
        url = reverse("company-managers-list-create", args=[self.company.id])
        data = {"company": self.company.id, "manager": new_user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyManager.objects.count(), 2)

    def test_deleting_manager(self):
        """Test a old manager deleting an new company manager"""
        self.client.force_authenticate(user=self.manager.manager)
        url = reverse(
            "company-manager-destroy",
            args=[self.manager.id],
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CompanyManager.objects.filter(id=self.manager.id).exists())

    def test_unauthorized_user_deleting_manager(self):
        """Test an unauthorized user deleting a company manager"""
        normal_user = UserFactory()
        self.client.force_authenticate(user=normal_user)
        url = reverse(
            "company-manager-destroy",
            args=[self.manager.id],
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
