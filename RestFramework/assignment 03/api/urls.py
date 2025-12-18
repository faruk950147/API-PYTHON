from django.urls import path
from info.views import (
    GenericAPIView,
    AdmissionInfoView,
)
urlpatterns = [
    path('', GenericAPIView.as_view()),
    path('admission-info/', AdmissionInfoView.as_view()),
]