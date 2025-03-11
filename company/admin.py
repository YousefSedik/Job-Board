from django.contrib import admin
from .models import Company, CompanyManager, CompanyOffice

admin.site.register(
    Company
)
admin.site.register(
    CompanyManager
)
admin.site.register(
    CompanyOffice
)