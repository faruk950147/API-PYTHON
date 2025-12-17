from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from admission.models import Student
from admission.serializers import StudentSerializer

class GeneralView(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the Admission API",
            "version": "1.0.0",
            "status": "running",
            "base_url": "http://127.0.0.1:8000/"
        })

class StudentAPIView(APIView):

    def get(self, request):
        student_id = request.data.get('id')
        if student_id:
            student = get_object_or_404(Student, id=student_id)
            serializer = StudentSerializer(student, many=False)
            return Response(serializer.data)
        else:
            student = Student.objects.all()
            serializer = StudentSerializer(student, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Student created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Failed to create student",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        student_id = request.data.get('id')
        if not student_id:
            return Response({
                "status": "error",
                "message": "Student ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        student = get_object_or_404(Student, id=student_id)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Student updated successfully",
                "data": serializer.data
            })
        return Response({
            "status": "error",
            "message": "Failed to update student",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        student_id = request.data.get('id')
        if not student_id:
            return Response({
                "status": "error",
                "message": "Student ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        student = get_object_or_404(Student, id=student_id)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Student updated successfully",
                "data": serializer.data
            })
        return Response({
            "status": "error",
            "message": "Failed to update student",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        student_id = request.data.get('id')
        if not student_id:
            return Response({
                "status": "error",
                "message": "Student ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        student = get_object_or_404(Student, id=student_id)
        student.delete()
        return Response({
            "status": "success",
            "message": "Student deleted successfully"
        }, status=status.HTTP_200_OK)
