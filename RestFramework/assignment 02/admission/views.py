from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from admission.models import Student
from admission.serializers import StudentSerializer 


class GeneralView(APIView):
    """
    General API Information View.
    
    Returns API status, version, base URL, and available endpoints.
    """
    def get(self, request):
        return Response({
            "message": "Welcome to the Admission API",
            "version": "1.0.0",
            "status": "running",
            "base_url": "http://127.0.0.1:8000/",
            "endpoints": [
                "/student/add/",
                "/student/update/<id>/",
                "/student/delete/<id>/",
                "/student/detail/<id>/",
                "/students/list/",
            ]
        }, status=status.HTTP_200_OK)


class StudentAddView(APIView):
    """
    Add a new student.
    
    POST data example:
    {
        "name": "John Doe",
        "age": 18,
        "grade": "A"
    }
    """
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Student added successfully",
                "student": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class StudentUpdateView(APIView):
    """
    Update an existing student by ID.
    
    PUT data example:
    {
        "name": "Jane Doe",
        "age": 19
    }
    """
    def put(self, request, id):
        student = get_object_or_404(Student, id=id)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Student updated successfully",
                "student": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class StudentDeleteView(APIView):
    """
    Delete a student by ID.
    """
    def delete(self, request, id):
        student = get_object_or_404(Student, id=id)
        student.delete()
        return Response({
            "status": "success",
            "message": "Student deleted successfully"
        }, status=status.HTTP_200_OK)


class StudentListView(APIView):
    """
    List all students.
    """
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response({
            "status": "success",
            "students": serializer.data
        }, status=status.HTTP_200_OK)


class StudentDetailView(APIView):
    """
    Retrieve a single student by ID.
    """
    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        serializer = StudentSerializer(student)
        return Response({
            "status": "success",
            "student": serializer.data
        }, status=status.HTTP_200_OK)