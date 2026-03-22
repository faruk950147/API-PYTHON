from django.urls import path
from official.views import (
    PostAPIView   
)

urlpatterns = [
   path('', PostAPIView.as_view())
]