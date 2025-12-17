from django.urls import path
from admission.views import UrlsView, RegistrationView

urlpatterns = [
    path('', UrlsView.as_view()),
    path('registration/', RegistrationView.as_view()),
]