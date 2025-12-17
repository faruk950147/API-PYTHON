from django.urls import path
from admission.views import (
    GeneralView, 
    StudentAddView, 
    StudentUpdateView, 
    StudentDeleteView, 
    StudentListView, 
    StudentDetailView
)

urlpatterns = [
    path('', GeneralView.as_view()),
    path('student/add/', StudentAddView.as_view()),
    path('student/update/<int:id>/', StudentUpdateView.as_view()),
    path('student/delete/<int:id>/', StudentDeleteView.as_view()),
    path('students/list/', StudentListView.as_view()),
    path('student/detail/<int:id>/', StudentDetailView.as_view()),
]