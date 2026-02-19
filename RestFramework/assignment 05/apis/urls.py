from django.urls import path
from apis.views import AdmissionInfoView, AdmissionInfoEditView, AdmissionInfoDeleteView

urlpatterns = [
    path('admission-info/', AdmissionInfoView.as_view(), name='admission-info'),
    path('admission-info-edit/<int:id>/', AdmissionInfoEditView.as_view(), name='admission-info-edit'),
    path('admission-info-delete/<int:id>/', AdmissionInfoDeleteView.as_view(), name='admission-info-delete'),
]