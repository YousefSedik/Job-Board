from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework import generics
from .serializers import (
    BookmarkCreateSerializer,
    BookmarkSerializersList,
    BookmarkDestroySerializers,
    JobSerializer,
    JobCreateSerializer,
    JobApplicationSerializer,
    JobApplicationListSerializer,
    JobApplicationUpdateSerializer,
    JobUpdateSerializer,
)
from rest_framework import permissions, response, status
from .models import JobBookmark, Job, JobApplication
from .permissions import IsObjectOwner, IsCompanyManager
from rest_framework.exceptions import PermissionDenied
from company.models import CompanyManager, CompanyOffice


class BookmarkCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkCreateSerializer


class BookmarkDestroyAPIView(DestroyAPIView):
    serializer_class = BookmarkDestroySerializers
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    queryset = JobBookmark.objects.all()


class BookmarkListAPIView(ListAPIView):
    serializer_class = BookmarkSerializersList
    queryset = JobBookmark.objects.all()

    def get_queryset(self):
        return JobBookmark.objects.filter(user=self.request.user)


class JobDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return JobUpdateSerializer
        elif self.request.method == "GET":
            return JobSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [permissions.IsAuthenticated, IsCompanyManager]
        return super().get_permissions()


class JobCreateAPIView(CreateAPIView):
    serializer_class = JobCreateSerializer
    queryset = Job.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DjangoValidationError as e:
            if hasattr(e, "message_dict"):
                error_detail = e.message_dict
            else:
                error_detail = {
                    "error": (
                        [str(m) for m in e.messages]
                        if hasattr(e, "messages")
                        else [str(e)]
                    )
                }

            return response.Response(error_detail, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        company_office = self.request.data.get("company_office")
        company_office = CompanyOffice.objects.get(id=company_office)
        is_manager = CompanyManager.objects.filter(
            company=company_office.company.id, manager=self.request.user
        ).exists()
        if not is_manager:
            raise PermissionDenied("Only managers of this company can create jobs.")

        serializer.save(created_by=self.request.user)


class JobApplicationAPIView(CreateAPIView):
    serializer_class = JobApplicationSerializer
    queryset = JobApplication.objects.all()


class JobApplicationUpdateAPIView(generics.UpdateAPIView):
    serializer_class = JobApplicationUpdateSerializer
    queryset = JobApplication.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsCompanyManager]

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DjangoValidationError as e:
            if hasattr(e, "message_dict"):
                error_detail = e.message_dict
            else:
                error_detail = {
                    "error": (
                        [str(m) for m in e.messages]
                        if hasattr(e, "messages")
                        else [str(e)]
                    )
                }

            return response.Response(error_detail, status=status.HTTP_400_BAD_REQUEST)


class JobApplicationListAPIView(ListAPIView):
    serializer_class = JobApplicationListSerializer
    queryset = JobApplication.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
