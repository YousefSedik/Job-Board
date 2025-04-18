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
from rest_framework import authentication
from .models import JobBookmark, Job, JobRequirement, JobResponsibility, Application
from .permissions import IsCompanyManager, IsObjectOwner


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
    permission_classes = [permissions.IsAuthenticated, IsCompanyManager]


class JobApplicationAPIView(CreateAPIView):
    serializer_class = JobApplicationSerializer
    queryset = Application.objects.all()
