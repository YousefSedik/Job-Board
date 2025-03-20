from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CompanyOffice(models.Model):
    country = models.ForeignKey(
        "cities_light.Country", on_delete=models.SET_NULL, null=True, blank=True
    )
    city = models.ForeignKey(
        "cities_light.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="offices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company.name + " - " + self.city.name + ", " + self.country.name


class Company(models.Model):
    class NumberOfEmployees(models.IntegerChoices):
        _1_10 = 1, "1-10"
        _11_50 = 2, "11-50"
        _51_200 = 3, "51-200"
        _201_500 = 4, "201-500"
        _501_1000 = 5, "501-1000"
        _1001_5000 = 6, "1001-5000"
        _5001_10000 = 7, "5001-10000"
        _10001_plus = 8, "10001+"

    name = models.CharField(max_length=255)
    about = models.TextField()
    profile_image = models.ImageField(
        upload_to="company/profile_image/", null=True, blank=True
    )
    number_of_employees = models.PositiveBigIntegerField(
        choices=NumberOfEmployees.choices, default=NumberOfEmployees._1_10
    )
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyManager(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company.name + " - " + self.manager.email
