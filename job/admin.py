from django.contrib import admin
from .models import Job, JobBookmark, JobRequirement, JobResponsibility, JobApplication

admin.site.register(JobBookmark)
admin.site.register(JobRequirement)
admin.site.register(JobResponsibility)


class JobModelAdmin(admin.ModelAdmin):
    search_fields = ("company", "company_office")
    list_display = (
        "title",
        "company",
        "created_at",
        "updated_at",
        "number_of_applicants",
    )
    list_filter = ("company", "created_at", "updated_at")
    autocomplete_fields = ("company", "company_office")


class JobApplicationModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        "user",
        "job",
        "created_at",
        "updated_at",
        "is_cover_letter_ai_generated",
    )
    readonly_fields = (
        "cover_letter",
        "status",
        "resume",
        "created_at",
        "updated_at",
        "is_cover_letter_ai_generated",
        "is_cover_letter_ai_report",
        "job",
        "user",
    )
    list_filter = ("job", "created_at", "updated_at", "is_cover_letter_ai_generated")
    search_fields = ("user__email", "job__title", "job__company__name", "resume__user")
    ordering = ("-created_at",)
    autocomplete_fields = ("job", "user", "resume")

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            self.readonly_fields = ()
        return super().get_readonly_fields(request, obj)


admin.site.register(JobApplication, JobApplicationModelAdmin)
admin.site.register(Job, JobModelAdmin)
