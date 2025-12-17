from django.urls import path
from admission.views import GeneralView, StudentAPIView

urlpatterns = [
    path('', GeneralView.as_view()),
    path('students/', StudentAPIView.as_view()),
]