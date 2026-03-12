from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apis.models import Student
from apis.serializers import StudentSerializer

class StudentsView(APIView):
    def get(self, request, pk=None, format=None):
        if pk:
            student = get_object_or_404(Student, pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)