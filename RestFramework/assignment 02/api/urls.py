from django.urls import path
from rest_framework.views import csrf_exempt
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
    path('student/add/', csrf_exempt(StudentAddView.as_view())),
    path('student/update/<int:id>/', csrf_exempt(StudentUpdateView.as_view())),
    path('student/delete/<int:id>/', csrf_exempt(StudentDeleteView.as_view())),
    path('students/list/', StudentListView.as_view()),
    path('student/detail/<int:id>/', StudentDetailView.as_view()),
]