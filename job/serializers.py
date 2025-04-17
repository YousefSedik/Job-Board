from rest_framework import serializers
from .models import JobBookmark, Job, JobRequirement, JobResponsibility, Application
from company.serializers import CompanySerializer, CompanyOfficeSerializer


class BookmarkSerializersList(serializers.ModelSerializer):
    job = serializers.HyperlinkedRelatedField(
        view_name="job-detail", lookup_field="id", read_only=True
    )

    class Meta:
        model = JobBookmark
        fields = ["job", "created_at", "id"]


class BookmarkCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = JobBookmark
        fields = ["job", "user"]

    def validate(self, attrs):
        user = self.context["request"].user
        job = attrs["job"]

        if JobBookmark.objects.filter(user=user, job=job).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["You have already bookmarked this job."]}
            )

        return attrs


class BookmarkDestroySerializers(serializers.ModelSerializer):
    class Meta:
        model = JobBookmark
        fields = ["job"]


class JobSerializer(serializers.ModelSerializer):
    company_office = CompanyOfficeSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    job_type = serializers.CharField(source="get_job_type_display", read_only=True)
    work_place = serializers.CharField(source="get_work_place_display", read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "title",
            "overview",
            "salary_start_from",
            "salary_end",
            "job_type",
            "work_place",
            "company_office",
        ]

    def validate(self, attrs):
        if attrs["salary_start_from"] > attrs["salary_end"]:
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "Salary start from must be less than salary end."
                    ]
                }
            )
        return attrs


class JobRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequirement
        fields = ["description"]


class JobResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResponsibility
        fields = ["description"]


class JobApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Application
        fields = ["user", "job", "resume", "cover_letter"]
