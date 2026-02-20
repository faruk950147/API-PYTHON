from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apis.models import Student
from apis.serializers import StudentSerializer

class StudenstView(APIView):
    def get(self, request, pk=None):
        pass
