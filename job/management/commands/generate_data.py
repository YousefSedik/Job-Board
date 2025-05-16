from django.core.management.base import BaseCommand
from job.factories import JobFactory, JobApplicationFactory
from company.factories import CompanyFactory, CompanyOfficeFactory


class Command(BaseCommand):
    help = "generate random data"

    def handle(self, *args, **kwargs):
        # generate 20 companies
        companies = [CompanyFactory() for c in range(20)]
        self.stdout.write("Generated 20 Company Objects")
        # generate 5 offices for each company
        offices = [
            [CompanyOfficeFactory(company=company) for i in range(5)]
            for company in companies
        ]
        # generate 20 jobs for each office
        jobs = [
            [JobFactory(company_office=company_office) for company_office in company]
            for company in offices
        ]
        # generate applications
        for g in jobs:
            for job in g:
                for i in range(10):
                    JobApplicationFactory(job=job)
