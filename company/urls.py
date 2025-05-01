from django.urls import path
from .api import (
    CompanyRetrieveUpdateAPIView,
    CompanyManagerListCreateAPIView,
    CompanyManagerDestroyAPIView,
)

urlpatterns = [
    path(
        "api/company/<int:pk>",
        CompanyRetrieveUpdateAPIView.as_view(),
        name="company-retrieve-update",
    ),
    path(
        "api/company/<int:company_id>/managers",
        CompanyManagerListCreateAPIView.as_view(),
        name="company-managers-list-create",
    ),
    path(
        "api/company/managers/<int:pk>",
        CompanyManagerDestroyAPIView.as_view(),
        name="company-manager-destroy",
    ),
]
