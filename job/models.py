from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models

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
        "company.CompanyOffice",
        on_delete=models.CASCADE,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_jobs"
    )

    def save(self, *args, **kwargs):
        if self.salary_start_from > self.salary_end:
            raise ValidationError("Salary start from must be less than salary end.")
        if self.salary_start_from < 0 or self.salary_end < 0:
            raise ValidationError("Salary must be positive.")
        if self.salary_start_from == self.salary_end:
            raise ValidationError("Salary start from must be less than salary end.")
        self.company = self.company_office.company
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.company}"


class JobApplication(models.Model):

    class JobApplicationStatus(models.TextChoices):
        APPLIED = "A", "Applied"
        REJECTED = "R", "Rejected"
        INVITED = "I", "Invited"
        HIRED = "H", "Hired"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    resume = models.ForeignKey("users.Resume", on_delete=models.DO_NOTHING)
    cover_letter = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=8,
        choices=JobApplicationStatus.choices,
        default=JobApplicationStatus.APPLIED,
    )
    is_cover_letter_ai_generated = models.FloatField(
        null=True, blank=True, default=None
    )
    is_cover_letter_ai_report = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.job.title} - {self.status}"

    def clean(self):
        if self.pk:
            try:
                old = self.__class__.objects.get(pk=self.pk)
                options = {
                    "Applied": ["Rejected", "Invited", "Hired"],
                    "Invited": ["Rejected", "Hired"],
                    "Rejected": [],
                    "Hired": [],
                }
                if self.get_status_display() not in options[old.get_status_display()]:
                    raise ValidationError(
                        f"Cannot change status from {old.get_status_display()} to {self.get_status_display()}"
                    )

            except self.__class__.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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


@receiver(post_save, sender=JobApplication)
def increment_job_applicants(sender, instance, **kwargs):
    job = instance.job
    job.number_of_applicants += 1
    job.save()


@receiver(post_save, sender=JobApplication)  # start task
def start_is_cover_letter_ai_generated(sender, instance, created, **kwargs):
    if settings.TESTING:
        return
    if created:
        from job.tasks import is_cover_letter_ai_generated_task

        is_cover_letter_ai_generated_task.delay(instance.id)
