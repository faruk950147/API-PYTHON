from django.urls import path
from apis.views import (
    StudenstView,
)

urlpatterns = [
    path('students', StudenstView.as_view())
]