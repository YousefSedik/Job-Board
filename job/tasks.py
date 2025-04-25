from celery import shared_task
from .models import JobApplication
from .services import is_ai_generated_report


@shared_task
def is_cover_letter_ai_generated_task(job_application_id):
    job_application = JobApplication.objects.get(id=job_application_id)
    if len(job_application.cover_letter.split()) > 30:
        is_ai = is_ai_generated_report(job_application.cover_letter)
        job_application.is_cover_letter_ai_report = is_ai
        if is_ai["success"]:
            job_application.is_cover_letter_ai_generated = is_ai["data"][
                "fakePercentage"
            ]
        job_application.save()
