from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import(
    Task
)
from api.serializers import(
    TaskSerializer
)
# Create your views here.
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'Saved': 'TaskSaved/',
        'List': 'TaskList/',
        'Details': 'TaskDetails/<int:id>/',
        'Updated': 'TaskUpdated/<int:id>/',
        'Deleted': 'TaskDeleted/<int:id>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def TaskList(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def TaskDetails(request, id):
    task = get_object_or_404(Task, id=id)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def TaskSaved(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def TaskUpdated(request, id):
    task = get_object_or_404(Task, id=id)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def TaskDeleted(request, id):
    task = get_object_or_404(Task, id=id).delete()
    return Response('Task deleteed successfull')