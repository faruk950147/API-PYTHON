from django.shortcuts import render
from api.models import Task
# Create your views here.
def List(request):
    
    context = {
        
    }
    return render(request, 'task/list.html', context)