from django.urls import path
from admission.views import UrlsView, StudentAPIView

urlpatterns = [
    path('', UrlsView.as_view()),
    path('students/', StudentAPIView.as_view()),
]