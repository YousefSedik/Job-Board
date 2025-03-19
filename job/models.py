from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class JobResponsibility(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(
        "Job", on_delete=models.CASCADE, related_name="responsibilities"
    )

    def __str__(self):
        return self.description


class JobRequirement(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(
        "Job", on_delete=models.CASCADE, related_name="requirements"
    )

    def __str__(self):
        return self.description


class Job(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = "FT", "Full Time"
        PART_TIME = "PT", "Part Time"

    class WorkPlace(models.TextChoices):
        REMOTE = "RE", "Remote"
        OFFICE = "OF", "Office"
        HYBRID = "HY", "Hybrid"

    title = models.CharField(max_length=255)
    overview = models.TextField()
    salary_start_from = models.PositiveIntegerField()
    salary_end = models.PositiveIntegerField()
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
    number_of_applicants = models.PositiveIntegerField(default=0)
    job_type = models.CharField(max_length=2, choices=JobType.choices)
    work_place = models.CharField(max_length=6, choices=WorkPlace.choices)
    company_office = models.ForeignKey(
        "company.CompanyOffice", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=..., force_update=..., using=..., update_fields=...):
        self.company = self.company_office.company
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.title} - {self.company}"


class Application(models.Model):

    class ApplicationStatus(models.TextChoices):
        APPLIED = "A", "Applied"
        REJECTED = "R", "Rejected"
        INVITED = "I", "Invited"
        HIRED = "H", "Hired"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    resume = models.ForeignKey("users.Resume", on_delete=models.CASCADE)
    cover_letter = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=8,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED,
    )

    class Meta:
        unique_together = ["user", "job"]


class JobBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() + " - " + str(self.job.id)

    class Meta:
        unique_together = ["user", "job"]
