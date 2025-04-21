from rest_framework import permissions
from company.models import CompanyManager


from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied


class IsCompanyManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return CompanyManager.objects.filter(
            manager=request.user, company=obj.company
        ).exists()


class IsObjectOwner(permissions.BasePermission):
    owner_field = "user"

    def has_object_permission(self, request, view, obj):
        return getattr(obj, self.owner_field) == request.user
