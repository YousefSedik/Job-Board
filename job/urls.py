from django.urls import path
from .api import (
    BookmarkCreateAPIView,
    BookmarkDestroyAPIView,
    BookmarkListAPIView,
    JobDetailAPIView,
    JobCreateAPIView,
    JobApplicationAPIView,
)

urlpatterns = [
    path("bookmarks", BookmarkListAPIView.as_view(), name="list-bookmarks"),
    path("bookmark/<int:id>", BookmarkDestroyAPIView.as_view(), name="delete-bookmark"),
    path("bookmark", BookmarkCreateAPIView.as_view(), name="create-bookmark"),
    path("job/<int:id>", JobDetailAPIView.as_view(), name="job-detail"),
    path("job", JobCreateAPIView.as_view(), name="job-create"),
    path("job/apply", JobApplicationAPIView.as_view(), name="apply-job")
]
