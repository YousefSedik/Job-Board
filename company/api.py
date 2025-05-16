from rest_framework import generics, permissions
from .models import Company, CompanyManager
from .serializers import (
    CompanySerializer,
    CompanyUpdateSerializer,
    CompanyManagerSerializer,
)
from .permissions import IsManager
from .mixins import IsManagerMixins


class CompanyRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CompanyUpdateSerializer
        return CompanySerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated(), IsManager()]
        return [permissions.AllowAny()]


class CompanyManagerListCreateAPIView(IsManagerMixins, generics.ListCreateAPIView):
    queryset = CompanyManager.objects.all()
    serializer_class = CompanyManagerSerializer

    def get_queryset(self):
        return CompanyManager.objects.filter(company=self.kwargs["company_id"])


class CompanyManagerDestroyAPIView(IsManagerMixins, generics.DestroyAPIView):
    queryset = CompanyManager.objects.all()
