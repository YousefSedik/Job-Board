from celery import shared_task
from .models import Resume
from pypdf import PdfReader


@shared_task(bind=True)
def analyze_resume_task(resume_id):
    """
    Task to analyze a resume.
    """
    try:
        resume = Resume.objects.get(id=resume_id)
        print(f"Analyzing resume for user: {resume.user.email}")
        reader = PdfReader(resume.resume.path)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text = page.extract_text()
            print(f"Page {i + 1} text: {text}")
            resume.content += text + "\n"
        resume.save()

    except Resume.DoesNotExist:
        print(f"Resume with id {resume_id} does not exist.")

