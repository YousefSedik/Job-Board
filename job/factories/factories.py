from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
import factory.random
from job.models import Job, JobResponsibility, JobRequirement, JobBookmark
from users.factories import UserFactory
import factory
from factory import fuzzy

User = get_user_model()


class JobBookmarkFactory(DjangoModelFactory):
    class Meta:
        model = JobBookmark

    user = factory.SubFactory("users.factories.UserFactory")
    job = factory.SubFactory("job.factories.JobFactory")


class JobFactory(DjangoModelFactory):
    class Meta:
        model = Job

    title = factory.Faker("job")
    overview = factory.Faker("text")
    salary_start_from = factory.Faker("random_int", min=50000, max=100000)
    salary_end = factory.Faker("random_int", min=100000, max=200000)
    company = factory.SubFactory("company.factories.CompanyFactory")
    number_of_applicants = factory.Faker("random_int", min=0, max=100)
    job_type = fuzzy.FuzzyChoice([Job.JobType.FULL_TIME, Job.JobType.PART_TIME])
    work_place = fuzzy.FuzzyChoice(
        [Job.WorkPlace.REMOTE, Job.WorkPlace.OFFICE, Job.WorkPlace.HYBRID]
    )
    company_office = factory.SubFactory("company.factories.CompanyOfficeFactory")
