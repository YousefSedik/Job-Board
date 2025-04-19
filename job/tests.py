from .factories import JobBookmarkFactory, JobFactory
from users.factories import ResumeFactory, UserFactory
from rest_framework.test import APITestCase, APIClient
from users.factories import UserFactory
from rest_framework import status
from django.urls import reverse
from .models import JobBookmark, Job, JobRequirement, JobResponsibility, JobApplication


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
    # apply for job
    # what to test ?
    # 3. test apply for job with already applied job
    # 4. test apply for job with unauthorized user
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
