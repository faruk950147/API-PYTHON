from django.urls import path
from courses.views import (
    EndPointsListView,
    CoursesView
)

urlpatterns = [
    path('', EndPointsListView.as_view()),
    path('courses/', CoursesView.as_view())
]