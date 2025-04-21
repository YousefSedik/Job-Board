from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    CompanyViewSet,
    CompanyOfficeViewSet,
    CompanyManagerViewSet,
    CityViewSet,
    CountryViewSet,
)

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"offices", CompanyOfficeViewSet)
router.register(r"managers", CompanyManagerViewSet)
router.register(r"cities", CityViewSet)
router.register(r"countries", CountryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
