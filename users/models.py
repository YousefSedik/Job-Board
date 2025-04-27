from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timesince


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"
        ordering = ["-created_at"]

    @property
    def timesince(self):
        return timesince.timesince(self.created_at)

    def __str__(self):
        return self.user.email + " - " + self.resume.name


# import signals
from .tasks import analyze_resume_task


@receiver(post_save, sender=Resume)
def fire_resume_analyzer(sender, instance, created, **kwargs):
    if created:
        # call CV analysis service
        try:
            analyze_resume_task.delay(instance.id)
        except Exception:
            pass
