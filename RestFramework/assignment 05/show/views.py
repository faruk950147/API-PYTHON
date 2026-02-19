from django.shortcuts import render
from django.views import generic
from apis.models import Admission
# Create your views here.
class AdmissionListView(generic.View):
    def get(self, request):
        return render(request, 'show/admission-list.html')