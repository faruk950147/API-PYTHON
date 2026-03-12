from django.urls import path
from show.views import StudentListView

urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
]