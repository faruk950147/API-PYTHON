from django.urls import path
from apis.views import AdmissionInfoView

urlpatterns = [
    path('admission-info/', AdmissionInfoView.as_view(), name='admission-info'),
]