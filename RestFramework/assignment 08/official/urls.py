from django.urls import path
from official.views import (
    APIRoot,
)

urlpatterns = [
    # API Root
    path("", APIRoot.as_view(), name="api-root"),
]