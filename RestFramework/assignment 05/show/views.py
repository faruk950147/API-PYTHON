from django.shortcuts import render
from django.views import generic
from apis.models import Admission
# Create your views here.
class AdmissionListView(generic.View):
    def get(self, request):
        admissions = Admission.objects.filter(status='Active')
        return render(request, 'show/admission_list.html', {'admissions': admissions})