from django.urls import path
from office.views import (
    APIRoot,
)

urlpatterns = [
    # API Root
    path("", APIRoot.as_view(), name="api-root"),
]