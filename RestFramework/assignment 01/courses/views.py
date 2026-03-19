from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from courses.models import Courses
from courses.serializers import CoursesSerializer


class EndPointsListView(APIView):
    """
    API view to list all available API endpoints.
    """
    def get(self, request):
        """
        GET method to return a list of available API endpoints.
        """
        return Response({
            'status': 'success',
            'endPoints': [
                'http://127.0.0.1:8000/api/courses/'
            ]
        })


class CoursesView(APIView):
    """
    API view to handle CRUD operations for the Courses model.
    Supports GET, POST, PUT, PATCH, and DELETE HTTP methods.
    """

    def get_object(self, request):
        """
        Helper method to retrieve a Course instance by its ID from request data.
        Raises Http404 if the course does not exist.
        """
        course_id = request.data.get('id')
        if not course_id:
            return None
        try:
            return Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            raise Http404

    def get(self, request):
        """
        GET method to retrieve all courses.
        Returns a list of courses serialized in JSON format.
        """
        courses = Courses.objects.all()
        serializer = CoursesSerializer(courses, many=True)
        return Response({
            "msg": "Courses retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        POST method to create a new course.
        Expects course data in the request body.
        Returns the newly created course data if successful.
        """
        serializer = CoursesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Course created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT method to fully update an existing course.
        Expects the course ID in request data and updated course data.
        """
        course = self.get_object(request)
        if not course:
            return Response({"msg": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CoursesSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Course updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
        PATCH method to partially update an existing course.
        Expects the course ID in request data and the fields to update.
        """
        course = self.get_object(request)
        if not course:
            return Response({"msg": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CoursesSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Course partially updated",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        DELETE method to remove an existing course.
        Expects the course ID in request data.
        """
        course = self.get_object(request)
        if not course:
            return Response({"msg": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        course.delete()
        return Response({
            "msg": "Course deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)