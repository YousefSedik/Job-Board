from django.contrib import admin
from .models import Company, CompanyManager, CompanyOffice

from django.contrib import admin
# from cities_light.models import Country, City
# from cities_light.admin import CountryAdmin, CityAdmin


# class CountryAdmin(CountryAdmin):
#     search_fields = ["name"]


# class CityAdmin(CityAdmin):
    # search_fields = ["name"]


admin.site.register(Company)
admin.site.register(CompanyManager)


@admin.register(CompanyOffice)
class CompanyOfficeAdmin(admin.ModelAdmin):
    autocomplete_fields = ["country", "city"]
