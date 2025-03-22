from rest_framework import viewsets, permissions
from .models import Company, CompanyOffice, CompanyManager
from .serializers import (
    CompanySerializer,
    CompanyOfficeSerializer,
    CompanyManagerSerializer,
    CitySerializer,
    CountrySerializer,
)
from cities_light.models import City, Country
from rest_framework.decorators import action
from rest_framework.response import Response


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def offices(self, request, pk=None):
        company = self.get_object()
        offices = CompanyOffice.objects.filter(company=company)
        serializer = CompanyOfficeSerializer(offices, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def managers(self, request, pk=None):
        company = self.get_object()
        managers = CompanyManager.objects.filter(company=company)
        serializer = CompanyManagerSerializer(managers, many=True)
        return Response(serializer.data)


class CompanyOfficeViewSet(viewsets.ModelViewSet):
    queryset = CompanyOffice.objects.all()
    serializer_class = CompanyOfficeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CompanyOffice.objects.all()
        company_id = self.request.query_params.get("company_id", None)
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset


class CompanyManagerViewSet(viewsets.ModelViewSet):
    queryset = CompanyManager.objects.all()
    serializer_class = CompanyManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CompanyManager.objects.all()
        company_id = self.request.query_params.get("company_id", None)
        manager_id = self.request.query_params.get("manager_id", None)

        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        if manager_id is not None:
            queryset = queryset.filter(manager_id=manager_id)

        return queryset


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = City.objects.all()
        country_id = self.request.query_params.get("country_id", None)
        name = self.request.query_params.get("name", None)

        if country_id is not None:
            queryset = queryset.filter(country_id=country_id)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Country.objects.all()
        name = self.request.query_params.get("name", None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset
