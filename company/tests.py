from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Company, CompanyOffice, CompanyManager
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
        self.manager = CompanyManagerFactory(company=self.company)

    def test_list_companies(self):
        """Test retrieving a list of companies"""
        url = reverse("company-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_company(self):
        """Test creating a new company"""
        url = reverse("company-list")
        data = {
            "name": "New Test Company",
            "about": "This is a test company created for API testing",
            "number_of_employees": Company.NumberOfEmployees._11_50,
            "website": "https://newtestcompany.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(
            Company.objects.get(id=response.data["id"]).name, "New Test Company"
        )

    def test_retrieve_company(self):
        """Test retrieving a specific company"""
        url = reverse("company-detail", args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.company.name)

    def test_update_company(self):
        """Test updating a company"""
        url = reverse("company-detail", args=[self.company.id])
        data = {
            "name": "Updated Company Name",
            "about": self.company.about,
            "number_of_employees": self.company.number_of_employees,
            "website": self.company.website,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, "Updated Company Name")

    def test_delete_company(self):
        """Test deleting a company"""
        company_to_delete = CompanyFactory()
        url = reverse("company-detail", args=[company_to_delete.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(id=company_to_delete.id).exists())

    def test_company_offices_action(self):
        """Test the custom action to get company offices"""
        url = reverse("company-offices", args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.office.id)

    def test_company_managers_action(self):
        """Test the custom action to get company managers"""
        url = reverse("company-managers", args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.manager.id)


class CompanyOfficeAPITests(APITestCase):
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

    def test_list_offices(self):
        """Test retrieving a list of offices"""
        url = reverse("companyoffice-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_offices_by_company(self):
        """Test filtering offices by company"""
        # Create another company and office
        other_company = CompanyFactory()
        other_country = CountryFactory()
        other_city = CityFactory(country=other_country)
        # Make sure to pass all required fields explicitly
        CompanyOfficeFactory(
            company=other_company, country=other_country, city=other_city
        )

        url = f"{reverse('companyoffice-list')}?company_id={self.company.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.office.id)

    def test_create_office(self):
        """Test creating a new office"""
        url = reverse("companyoffice-list")
        data = {
            "company": self.company.id,
            "country": self.country.id,
            "city": self.city.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyOffice.objects.count(), 2)

    def test_update_office(self):
        """Test updating an office"""
        # Create a new city and country for updating
        new_country = CountryFactory()
        new_city = CityFactory(country=new_country)

        url = reverse("companyoffice-detail", args=[self.office.id])
        data = {
            "company": self.company.id,
            "country": new_country.id,
            "city": new_city.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.office.refresh_from_db()
        self.assertEqual(self.office.country.id, new_country.id)
        self.assertEqual(self.office.city.id, new_city.id)


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
        url = reverse("companymanager-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_managers_by_company(self):
        """Test filtering managers by company"""
        # Create another company and manager
        other_company = CompanyFactory()
        CompanyManagerFactory(company=other_company)

        url = f"{reverse('companymanager-list')}?company_id={self.company.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.manager.id)

    def test_create_manager(self):
        """Test creating a new company manager"""
        new_user = UserFactory()
        url = reverse("companymanager-list")
        data = {"company": self.company.id, "manager": new_user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyManager.objects.count(), 2)

    def test_delete_manager(self):
        """Test deleting a company manager"""
        url = reverse("companymanager-detail", args=[self.manager.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CompanyManager.objects.filter(id=self.manager.id).exists())


class CityAndCountryAPITests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create test data
        self.country = CountryFactory(name="United States")
        self.city1 = CityFactory(name="New York", country=self.country)
        self.city2 = CityFactory(name="Los Angeles", country=self.country)

        # Create another country
        self.other_country = CountryFactory(name="Canada")
        self.city3 = CityFactory(name="Toronto", country=self.other_country)

    def test_list_countries(self):
        """Test retrieving a list of countries"""
        url = reverse("country-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_filter_countries_by_name(self):
        """Test filtering countries by name"""
        url = f"{reverse('country-list')}?name=United"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "United States")

    def test_list_cities(self):
        """Test retrieving a list of cities"""
        url = reverse("city-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)

    def test_filter_cities_by_country(self):
        """Test filtering cities by country"""
        url = f"{reverse('city-list')}?country_id={self.country.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        city_names = [city["name"] for city in response.data]
        self.assertIn("New York", city_names)
        self.assertIn("Los Angeles", city_names)

    def test_filter_cities_by_name(self):
        """Test filtering cities by name"""
        url = f"{reverse('city-list')}?name=New"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "New York")
