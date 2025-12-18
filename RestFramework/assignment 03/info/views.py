from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class GenericAPIView(APIView):
    def get(self, request):
        return Response({"status": "success"})
    
class StudentInfoView(APIView):
    def get(self, request):
        return Response({"status": "success"})