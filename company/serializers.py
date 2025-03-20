from rest_framework import serializers
from .models import Company, CompanyOffice


class CompanySerializer(serializers.ModelSerializer):
    number_of_employees = serializers.CharField(
        source="get_number_of_employees_display", read_only=True
    )

    class Meta:
        model = Company
        fields = ["name", "about", "profile_image", "number_of_employees", "website"]


class CompanyOfficeSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="country.name", read_only=True)
    city = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = CompanyOffice
        fields = ["country", "city"]
