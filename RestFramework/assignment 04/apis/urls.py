from django.urls import path
from apis.views import (
    AdmissionListCreateAPIView, 
    AdmissionDetailAPIView
)

urlpatterns = [
    path('admissions/', AdmissionListCreateAPIView.as_view()),
    path('admissions/<int:pk>/', AdmissionDetailAPIView.as_view()),
]