from rest_framework import serializers
from .models import Company, CompanyOffice, CompanyManager
from cities_light.models import Country, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class CompanyOfficeSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source="city.name", read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = CompanyOffice
        fields = [
            "id",
            "company",
            "city",
            "country",
            "city_name",
            "country_name",
            "created_at",
            "updated_at",
        ]


class CompanySerializer(serializers.ModelSerializer):
    offices = CompanyOfficeSerializer(many=True, read_only=True)
    number_of_employees_display = serializers.CharField(
        source="get_number_of_employees_display", read_only=True
    )

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "about",
            "profile_image",
            "number_of_employees",
            "number_of_employees_display",
            "website",
            "offices",
            "created_at",
            "updated_at",
        ]


class CompanyManagerSerializer(serializers.ModelSerializer):
    manager_email = serializers.EmailField(source="manager.email", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = CompanyManager
        fields = [
            "id",
            "manager",
            "company",
            "manager_email",
            "company_name",
            "created_at",
        ]
