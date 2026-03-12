from django.shortcuts import render
from django.views import generic
from apis.models import Student
# Create your views here.
class StudentListView(generic.View):
    def get(self, request):
        return render(request, 'show/student-list.html')