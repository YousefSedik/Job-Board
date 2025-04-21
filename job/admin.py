from django.contrib import admin
from .models import Job, JobBookmark, JobRequirement, JobResponsibility, JobApplication

admin.site.register(Job)
admin.site.register(JobBookmark)
admin.site.register(JobRequirement)
admin.site.register(JobResponsibility)
admin.site.register(JobApplication)
