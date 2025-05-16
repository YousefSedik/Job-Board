from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager


class IsManagerMixins:
    permission_classes = [IsAuthenticated, IsManager]
