from admission.views import AdmissionUrlsView
from django.urls import path

urlpatterns = [
    path('admissions/', AdmissionUrlsView.as_view(), name='admission-urls'),
]