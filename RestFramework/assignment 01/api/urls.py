from django.urls import path
from courses.views import (
    EndPointsListView
)

urlpatterns = [
    path('', EndPointsListView.as_view)
]