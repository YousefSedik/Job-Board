import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from company.models import Company, CompanyOffice, CompanyManager
from cities_light.models import Country, City
import random
from users.factories import UserFactory
User = get_user_model()




class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country
        django_get_or_create = ("name",)

    name = factory.Faker("country")


class CityFactory(DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = ("name", "country")

    name = factory.Faker("city")
    country = factory.SubFactory(CountryFactory)


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    about = factory.Faker("paragraph", nb_sentences=5)
    website = factory.Faker("url")
    number_of_employees = factory.LazyFunction(
        lambda: random.choice(
            [choice[0] for choice in Company.NumberOfEmployees.choices]
        )
    )


class CompanyOfficeFactory(DjangoModelFactory):
    class Meta:
        model = CompanyOffice

    company = factory.SubFactory(CompanyFactory)
    country = factory.SubFactory(CountryFactory)
    city = factory.SubFactory(CityFactory, country=factory.SelfAttribute("..country"))


class CompanyManagerFactory(DjangoModelFactory):
    class Meta:
        model = CompanyManager

    company = factory.SubFactory(CompanyFactory)
    manager = factory.SubFactory(UserFactory)
