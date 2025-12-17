from django.urls import path
from admission.views import GeneralView, StudentAPIView

urlpatterns = [
    path('', GeneralView.as_view()),
    path('students/<int:id>/', StudentAPIView.as_view()),
]