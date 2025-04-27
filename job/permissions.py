from rest_framework import permissions
from company.models import CompanyManager


class IsCompanyManager(permissions.BasePermission):
    message = "Only managers of this company can create or update jobs."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        company = None
        if hasattr(obj, "get_company") and callable(getattr(obj, "get_company")):
            company = obj.get_company()

        if not company:
            return False

        return CompanyManager.objects.filter(
            manager=request.user, company=company
        ).exists()


class IsObjectOwner(permissions.BasePermission):
    owner_field = "user"

    def has_object_permission(self, request, view, obj):
        return getattr(obj, self.owner_field) == request.user
