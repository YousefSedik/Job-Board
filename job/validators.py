from rest_framework import serializers
from .models import JobApplication


job_user_unique = serializers.UniqueTogetherValidator(
    queryset=JobApplication.objects.all(),
    fields=["user", "job"],
    message="You've already applied to this job.",
)

