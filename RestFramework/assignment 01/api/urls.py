from courses.views import CourseListView
from django.urls import path
urlpatterns = [
    path('course-list', CourseListView.as_view(), name='course-list'),
]