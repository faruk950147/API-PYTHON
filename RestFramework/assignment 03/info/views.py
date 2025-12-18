from re import A
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from info.models import Admission
from info.serializers import AdmissionSerializer

# Create your views here.
class GenericAPIView(APIView):
    def get(self, request):
        return Response({"status": "success"})
    
def AdmissionInfoView(request):
    if request.method == 'GET':
        admissions = Admission.objects.all()
        serializer = AdmissionSerializer(admissions, many=True)
        return Response(serializer.data)
    
    data = request.data
    if request.method == 'POST':
        serializer = AdmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # PUT / PATCH / DELETE need id
    admission = get_object_or_404(Admission, id=data.get('id'))

    if request.method == 'PUT':
        serializer = AdmissionSerializer(admission, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = AdmissionSerializer(admission, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        admission.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)