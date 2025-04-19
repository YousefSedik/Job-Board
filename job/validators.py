from rest_framework import serializers
from .models import JobApplication


job_user_unique = serializers.UniqueTogetherValidator(
    queryset=JobApplication.objects.all(),
    fields=["user", "job"],
    message="You've already applied to this job.",
)


def validate_(resume, user):
    if resume.user != user:
        raise serializers.ValidationError("You are not the owner of this resume.")
    return resume
