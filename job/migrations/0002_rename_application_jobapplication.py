# Generated by Django 5.1.6 on 2025-04-19 10:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0001_initial"),
        ("users", "0003_resume_content"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Application",
            new_name="JobApplication",
        ),
    ]
