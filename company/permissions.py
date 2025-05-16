from rest_framework import permissions
from .models import CompanyManager


class IsManager(permissions.BasePermission):
    """
    Custom permission to only allow managers of a company to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET requests for all users.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the manager of the company.
        company = None
        if hasattr(obj, "get_company") and callable(getattr(obj, "get_company")):
            company = obj.get_company()
        # print(company)
        return CompanyManager.objects.filter(
            manager=request.user, company=company
        ).exists()

    def has_permission(self, request, view):
        # Allow GET requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow PUT, PATCH, DELETE requests only for managers
        return request.user.is_authenticated
