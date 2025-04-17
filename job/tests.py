from .factories import JobBookmarkFactory, JobFactory
from rest_framework.test import APITestCase
from users.factories import UserFactory
from rest_framework import status
from django.urls import reverse


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

    def delete_authorized_job_bookmark(self):
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

    def delete_unauthorized_job_bookmark(self):
        user = UserFactory()
        job = JobFactory()
        bookmark = JobBookmarkFactory(user=user, job=job)
        url = reverse("delete-bookmark", args=[bookmark.id])
        self.client.force_authenticate(user=None)

        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse("list-bookmarks")
        response = self.client.get(list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
