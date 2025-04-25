from .factories import JobBookmarkFactory, JobFactory, JobApplicationFactory
from users.factories import ResumeFactory, UserFactory
from rest_framework.test import APITestCase, APIClient
from users.factories import UserFactory
from rest_framework import status
from django.urls import reverse
from .models import JobBookmark, Job, JobRequirement, JobResponsibility, JobApplication
from faker import Faker
from company.factories import (
    CompanyFactory,
    CompanyManagerFactory,
    CompanyOfficeFactory,
)


class JobBookmarkTests(APITestCase):

    def test_create_job_bookmark(self):
        user = UserFactory()
        job = JobFactory()
        url = reverse("create-bookmark")
        self.client.force_authenticate(user=user)
        data = {
            "job": job.id,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        list_url = reverse("list-bookmarks")
        response = self.client.get(list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(
            response.data[0]["job"].endswith(reverse("job-detail", args=[job.id]))
        )

    def test_delete_owned_job_bookmark(self):
        user = UserFactory()
        job = JobFactory()
        bookmark = JobBookmarkFactory(user=user, job=job)
        url = reverse("delete-bookmark", args=[bookmark.id])
        self.client.force_authenticate(user=user)

        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("list-bookmarks")
        response = self.client.get(list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_delete_unowned_job_bookmark(self):
        self.client = APIClient()
        user = UserFactory()
        other_user = UserFactory()
        job = JobFactory()
        bookmark = JobBookmarkFactory(user=user, job=job)
        url = reverse("delete-bookmark", args=[bookmark.id])
        self.client.force_authenticate(user=None)

        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class JobApplicationTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.job = JobFactory()
        self.resume = ResumeFactory(user=self.user)
        self.resume2 = ResumeFactory(user=self.other_user)
        self.apply_job_url = reverse("apply-job")
        self.client.force_authenticate(user=self.user)

    def test_apply_with_valid_data(self):

        data = {
            "job": self.job.id,
            "resume": self.resume.id,
            "cover_letter": "I am very interested in this position.",
        }

        response = self.client.post(self.apply_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            JobApplication.objects.filter(user=self.user, job=self.job).count(), 1
        )

    def test_apply_with_invalid_cover_letter(self):
        data = {
            "job": self.job.id,
            "resume": self.resume.id,
            "cover_letter": "",
        }

        response = self.client.post(self.apply_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_with_unowned_resume(self):

        data = {
            "job": self.job.id,
            "resume": self.resume2.id,
            "cover_letter": "Hello",
        }

        response = self.client.post(self.apply_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_with_invalid_job_id(self):
        data = {
            "job": Job.objects.last().id + 1,
            "resume": self.resume.id,
            "cover_letter": "Hello",
        }

        response = self.client.post(self.apply_job_url, data, format="json")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data.get("job", [""])[0], "Job Doesn't Exists")

    def test_apply_twice(self):
        user = UserFactory()
        job = JobFactory()
        resume = ResumeFactory(user=user)
        self.client.force_authenticate(user=user)
        data = {"job": job.id, "cover_letter": "Hello", "resume": resume.id}
        response = self.client.post(self.apply_job_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.apply_job_url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            "You've already applied to this job." in data.get("non_field_errors", [])
        )


class JobCreationTests(APITestCase):
    def setUp(self):
        self.faker = Faker()
        self.create_job_url = reverse("job-create")
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.company = CompanyFactory()
        self.company_office = CompanyOfficeFactory(company=self.company)
        self.company_manger = CompanyManagerFactory(
            company=self.company, manager=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.default_data = {
            "title": self.faker.word(),
            "overview": self.faker.paragraph(),
            "salary_start_from": 10000,
            "salary_end": 15000,
            "job_type": Job.JobType.FULL_TIME,
            "work_place": Job.WorkPlace.HYBRID,
            "company_office": self.company_office.id,
        }
        return super().setUp()

    def test_authorized_manager_create_a_job(self):
        data = self.default_data.copy()
        response = self.client.post(self.create_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_manager_create_a_job(self):
        data = self.default_data.copy()
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.create_job_url, data)
        data = response.json()
        self.assertEqual(
            data.get("detail", ""), "Only managers of this company can create jobs."
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_create_a_job(self):
        data = self.default_data.copy()
        self.client.force_authenticate(user=None)
        response = self.client.post(self.create_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateJobApplicationStatusTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.manager = UserFactory()
        self.company = CompanyFactory()
        self.company_office = CompanyOfficeFactory(company=self.company)
        self.company_manger = CompanyManagerFactory(
            company=self.company, manager=self.manager
        )
        self.job = JobFactory(
            company=self.company,
            company_office=self.company_office,
            created_by=self.manager,
        )
        self.resume = ResumeFactory(user=self.user)
        self.job_application = JobApplicationFactory(
            resume=self.resume,
            job=self.job,
        )
        self.update_url = reverse(
            "job-application-update", args=[self.job_application.id]
        )
        self.client.force_authenticate(user=self.manager)

    def test_manager_updating_job_application_with_valid_status(self):
        """
        Valid status transitions:
        APPLIED -> REJECTED
        APPLIED -> INVITED
        APPLIED -> HIRED
        INVITED -> REJECTED
        INVITED -> HIRED
        """
        combinations = [
            [
                {"status": "R", "status_code": 200},
                {"status": "I", "status_code": 400},
                {"status": "H", "status_code": 400},
            ],
            [
                {"status": "I", "status_code": 200},
                {"status": "R", "status_code": 200},
                {"status": "H", "status_code": 400},
            ],
            [
                {"status": "I", "status_code": 200},
                {"status": "H", "status_code": 200},
                {"status": "R", "status_code": 400},
            ],
            [
                {"status": "H", "status_code": 200},
                {"status": "I", "status_code": 400},
                {"status": "R", "status_code": 400},
            ],
        ]
        for combo in combinations:
            with self.subTest(combo=combo):
                # new job application object
                self.job = JobFactory(
                    company=self.company,
                    company_office=self.company_office,
                    created_by=self.manager,
                )
                self.job_application = JobApplicationFactory(job=self.job)
                self.update_url = reverse(
                    "job-application-update", args=[self.job_application.id]
                )
                for status in combo:
                    data = {"status": status["status"]}
                    response = self.client.patch(
                        self.update_url, data=data, format="json"
                    )
                    self.assertEqual(response.status_code, status["status_code"])
                    if status["status_code"] == 200:
                        self.job_application.refresh_from_db()
                        self.assertEqual(self.job_application.status, status["status"])

    def test_not_manager_updating_job_application_status(self):
        self.client.force_authenticate(user=self.other_user)
        combinations = [
            {"status": "R", "status_code": 403},
            {"status": "I", "status_code": 403},
            {"status": "H", "status_code": 403},
        ]
        self.job = JobFactory(
            company=self.company,
            company_office=self.company_office,
            created_by=self.manager,
        )
        self.job_application = JobApplicationFactory(job=self.job)
        self.update_url = reverse(
            "job-application-update", args=[self.job_application.id]
        )
        for status in combinations:
            data = {"status": status["status"]}
            response = self.client.patch(self.update_url, data=data, format="json")
            self.assertEqual(response.status_code, status["status_code"])
