from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
)
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
    ListJobApplicationsSerializer,
)
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from .models import JobBookmark, Job, JobApplication
from .permissions import IsObjectOwner, IsCompanyManager, IsCompanyManagerStrict
from rest_framework.exceptions import PermissionDenied
from company.models import CompanyManager, CompanyOffice
from django.shortcuts import get_object_or_404


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
        elif self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

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

            return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)


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

            return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        company_office = self.request.data.get("company_office")
        company_office = CompanyOffice.objects.get(id=company_office)
        is_manager = CompanyManager.objects.filter(
            company=company_office.company.id, manager=self.request.user
        ).exists()
        if not is_manager:
            raise PermissionDenied(
                "Only managers of this company can create or update jobs."
            )

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

            return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)


class JobApplicationListAPIView(ListAPIView):
    serializer_class = JobApplicationListSerializer
    queryset = JobApplication.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)


class ListJobApplicationsAPIView(ListAPIView):
    serializer_class = ListJobApplicationsSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyManagerStrict]

    def get_queryset(self):
        job = get_object_or_404(Job, id=self.kwargs["pk"])
        self.check_object_permissions(self.request, job)
        return JobApplication.objects.filter(job=job).order_by(
            "is_cover_letter_ai_generated"
        )
