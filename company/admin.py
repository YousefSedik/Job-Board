from django.contrib import admin
from .models import Company, CompanyManager, CompanyOffice


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(CompanyManager)
class CompanyManagerAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "company__name")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(CompanyOffice)
class CompanyOfficeAdmin(admin.ModelAdmin):
    autocomplete_fields = ["country", "city"]
    search_fields = ["name", "address"]
