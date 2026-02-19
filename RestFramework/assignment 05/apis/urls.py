from django.urls import path
from apis.views import (
    AdmissionInfoView,
    AdmissionInfoEditView,
    AdmissionInfoDeleteView
)

urlpatterns = [
    path('admission-info/', AdmissionInfoView.as_view()),
    path('admission-info/<int:id>/', AdmissionInfoEditView.as_view()),
    path('admission-info/<int:id>/', AdmissionInfoDeleteView.as_view()),
]