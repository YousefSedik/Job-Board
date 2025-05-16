from rest_framework import serializers
from users.models import Resume
from .models import JobBookmark, Job, JobRequirement, JobResponsibility, JobApplication
from company.serializers import CompanySerializer
from .validators import job_user_unique
from users.serializers import UserSerializer
from company.serializers import CompanyOfficeSerializer


class JobRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequirement
        fields = ["description"]


class JobResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResponsibility
        fields = ["description"]


class BookmarkSerializersList(serializers.ModelSerializer):
    job = serializers.HyperlinkedRelatedField(
        view_name="job-detail-update", read_only=True
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
    company = CompanySerializer(read_only=True)
    job_type = serializers.CharField(source="get_job_type_display", read_only=True)
    work_place = serializers.CharField(source="get_work_place_display", read_only=True)
    requirements = JobRequirementSerializer(many=True, read_only=True)
    responsibilities = JobResponsibilitySerializer(many=True, read_only=True)
    company_office = CompanyOfficeSerializer(read_only=True)

    class Meta:
        model = Job
        exclude = ["created_by"]
        # fields = "__all__"


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


class JobApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = JobApplication
        fields = ["user", "job", "resume", "cover_letter"]
        validators = [job_user_unique]
        extra_kwargs = {
            "job": {
                "error_messages": {
                    "does_not_exist": "Job Doesn't Exists",
                    "invalid": "Invalid value.",
                }
            }
        }

    def validate(self, attrs):
        user = self.context["request"].user
        resume = attrs["resume"]
        resume = Resume.objects.get(id=resume.id)
        if resume is None or resume.user != user:
            raise serializers.ValidationError("Resume does not exist.")

        return super().validate(attrs)


class JobApplicationListSerializer(serializers.ModelSerializer):
    job = serializers.HyperlinkedRelatedField(
        view_name="job-detail-update", read_only=True
    )
    resume = serializers.HyperlinkedRelatedField(
        view_name="users:retrieve-destroy-resume", read_only=True
    )
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = JobApplication
        fields = ["job", "resume", "cover_letter", "created_at", "updated_at", "status"]


class JobApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["status"]


class JobUpdateSerializer(serializers.ModelSerializer):
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


class ListJobApplicationsSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(source="resume.resume", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)
    user = UserSerializer()

    class Meta:
        model = JobApplication
        fields = [
            "resume",
            "status",
            "cover_letter",
            "user",
            "is_cover_letter_ai_generated",
        ]
