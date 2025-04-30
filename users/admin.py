from django.contrib import admin
from .models import Resume, CustomUser


class ResumeInline(admin.TabularInline):
    model = Resume
    extra = 1
    fields = ("resume", "created_at", "content")
    readonly_fields = ("created_at",)
    can_delete = False
    show_change_link = True
    max_num = 1


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)
    inlines = [ResumeInline]


class ResumeModelAdmin(admin.ModelAdmin):
    list_display = ("user", "resume", "created_at", "content")
    search_fields = ("user__email",)
    ordering = ("-created_at",)
    list_filter = ("created_at",)


admin.site.register(Resume, ResumeModelAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
