from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from admission.models import Student
from admission.serializers import StudentSerializer 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class GeneralView(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the Admission API",
            "version": "1.0.0",
            "status": "running",
            "base_url": "http://127.0.0.1:8000/"
        })


class StudentAPIView(APIView):
    def get(self, request, id=None):
        if id:
            student = get_object_or_404(Student, id=id)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Student created successfully",
                "status": "success"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "error": "Invalid data",
            "details": serializer.errors,
            "status": "error"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        student = get_object_or_404(Student, id=id)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Student updated successfully",
                "status": "success"
            }, status=status.HTTP_200_OK)
        return Response({
                "error": "Invalid data",
                "details": serializer.errors,
                "status": "error"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        student = get_object_or_404(Student, id=id)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "Student updated successfully",
                "status": "success"
            }, status=status.HTTP_200_OK)
        return Response({
            "error": "Invalid data",
            "details": serializer.errors,
            "status": "error"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        student = get_object_or_404(Student, id=id)
        student.delete()
        return Response({
            "message": "Deleted successfully",
            "status": "success"
        }, status=status.HTTP_200_OK)
