from django.urls import path
from info.views import (
    EndPointAPIView,
    AdmissionInfoView,
)
urlpatterns = [
    path('', EndPointAPIView.as_view()),
    path('admission-info/', AdmissionInfoView.as_view()),
]