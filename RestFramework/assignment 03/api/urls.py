from django.urls import path
from info.views import (
    GenericAPIView,
    StudentInfoView,
)
urlpatterns = [
    path('', GenericAPIView.as_view()),
    path('student-info/', StudentInfoView.as_view()),
]