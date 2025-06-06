from django.urls import path
from .api import (
    BookmarkCreateAPIView,
    BookmarkDestroyAPIView,
    BookmarkListAPIView,
    JobDetailUpdateAPIView,
    JobCreateAPIView,
    JobApplicationAPIView,
    JobApplicationListAPIView,
    JobApplicationUpdateAPIView,
    ListJobApplicationsAPIView,
)

urlpatterns = [
    path("bookmarks", BookmarkListAPIView.as_view(), name="list-bookmarks"),
    path("bookmark/<int:pk>", BookmarkDestroyAPIView.as_view(), name="delete-bookmark"),
    path("bookmark", BookmarkCreateAPIView.as_view(), name="create-bookmark"),
    path("job/<int:pk>", JobDetailUpdateAPIView.as_view(), name="job-detail-update"),
    path("job", JobCreateAPIView.as_view(), name="job-create"),
    path("job/apply", JobApplicationAPIView.as_view(), name="apply-job"),
    path(
        "job-applications",
        JobApplicationListAPIView.as_view(),
        name="list-applications",
    ),
    path(
        "job-application/<int:pk>",
        JobApplicationUpdateAPIView.as_view(),
        name="job-application-update",
    ),
    path(
        "job/<int:pk>/applications",
        ListJobApplicationsAPIView.as_view(),
        name="list-job-applications",
    ),
]
