from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from .serializers import (
    BookmarkCreateSerializer,
    BookmarkSerializersList,
    BookmarkDestroySerializers,
    JobSerializer,
    JobCreateSerializer,
    JobApplicationSerializer,
)
from rest_framework import permissions
from .models import JobBookmark, Job, JobApplication
from .permissions import IsObjectOwner
from rest_framework.exceptions import PermissionDenied
from company.models import CompanyManager, CompanyOffice


class BookmarkCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkCreateSerializer


class BookmarkDestroyAPIView(DestroyAPIView):
    serializer_class = BookmarkDestroySerializers
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]
    queryset = JobBookmark.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "id"


class BookmarkListAPIView(ListAPIView):
    serializer_class = BookmarkSerializersList
    queryset = JobBookmark.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class JobDetailAPIView(RetrieveAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "id"


class JobCreateAPIView(CreateAPIView):
    serializer_class = JobCreateSerializer
    queryset = Job.objects.all()
    permission_classes = [permissions.IsAuthenticated]

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
