from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, ResumeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Resume
from .permissions import OwnerOnly

User = get_user_model()


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


create_user = CreateUserView.as_view()


class UserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


get_user_profile = UserProfileAPIView.as_view()


class ResumeListCreateAPIView(ListCreateAPIView):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


resume_create_list_api_view = ResumeListCreateAPIView.as_view()


class ResumeRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
    permission_classes = [permissions.IsAuthenticated, OwnerOnly]


resume_retrieve_destroy_api_view = ResumeRetrieveDestroyAPIView.as_view()
