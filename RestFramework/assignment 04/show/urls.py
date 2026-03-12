from django.urls import path
from show.views import AdmissionListView

urlpatterns = [
    path('', AdmissionListView.as_view(), name='admission-list'),
]