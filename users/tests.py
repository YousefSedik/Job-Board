from django.core.files.uploadedfile import SimpleUploadedFile
from users.factories import ResumeFactory, UserFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import Resume


User = get_user_model()


class UsersManagersTests(APITestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com",
            password="foo",
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com",
            password="foo",
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


class UsersTestCases(APITestCase):
    def test_registering_users(self):
        # create user1, user2
        self.user1 = {
            "first_name": "yousef",
            "last_name": "sedik",
            "email": "random_email@gmail.com",
            "password": "strong_password1@",
            "password2": "strong_password1@",
        }
        self.client.post(reverse("users:create_user"), data=self.user1)

        self.assertEqual(User.objects.all().count(), 1)


class ResumeAPITest(APITestCase):
    def setUp(self):

        # Create users
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        # Create a resume for user1
        self.resume1 = ResumeFactory(user=self.user1)
        self.resume2 = ResumeFactory(user=self.user2)
        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

    def test_create_resume(self):
        """Test that a user can create a resume"""
        response = self.client.post(
            reverse("users:create-list-resume"),
            data={"resume": SimpleUploadedFile("test.pdf", b"file_content")},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Resume.objects.count(), 3)

    def test_access_own_resumes(self):
        """Test that a user can access their own resumes"""
        response = self.client.get(reverse("users:create-list-resume"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Should only see their own resume

    def test_delete_own_resume(self):
        """Test that a user can delete their own resume"""
        response = self.client.delete(
            reverse("users:retrieve-destroy-resume", args=[self.resume1.id])
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Resume.objects.filter(id=self.resume1.id).exists())
        # Check that the resume is deleted
        self.assertEqual(Resume.objects.count(), 1)

    def test_cannot_delete_other_user_resume(self):
        """Test that a user cannot delete someone else's resume"""
        self.client.force_authenticate(user=self.user2)  # Switch user
        response = self.client.delete(
            reverse("users:retrieve-destroy-resume", args=[self.resume1.id])
        )
        self.assertEqual(response.status_code, 403)  # Forbidden
        self.assertEqual(Resume.objects.count(), 2)
