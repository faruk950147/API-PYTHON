from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from django.core.paginator import Paginator
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

'''
class CoursesView(APIView):
    """
    # API view to handle CRUD operations for the Courses model.
    # Supports GET, POST, PUT, PATCH, and DELETE HTTP methods.
    """

    def get_object(self, request):
        """
        # Helper method to retrieve a Course instance by its ID from request data.
        # Raises Http404 if the course does not exist.
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
        # GET method to retrieve all courses.
        # Returns a list of courses serialized in JSON format.
        """
        courses = Courses.objects.all()
        serializer = CoursesSerializer(courses, many=True)
        return Response({
            "msg": "Courses retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        # POST method to create a new course.
        # Expects course data in the request body.
        # Returns the newly created course data if successful.
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
        # PUT method to fully update an existing course.
        # Expects the course ID in request data and updated course data.
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
        # DELETE method to remove an existing course.
        # Expects the course ID in request data.
        """
        course = self.get_object(request)
        if not course:
            return Response({"msg": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        course.delete()
        return Response({
            "msg": "Course deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
'''



class CoursesView(APIView):

    def get_object(self, course_id):
        try:
            return Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            raise Http404

    # GET (single + all + search + pagination)
    def get(self, request):
        course_id = request.query_params.get('id')
        search = request.query_params.get('search')
        page = request.query_params.get('page', 1)

        # Single Course
        if course_id:
            course = self.get_object(course_id)
            serializer = CoursesSerializer(course)
            return Response({
                "msg": "Single course",
                "data": serializer.data
            })

        # All Courses
        courses = Courses.objects.all()

        # Search
        if search:
            courses = courses.filter(title__icontains=search)

        # Pagination
        paginator = Paginator(courses, 5)  # প্রতি page এ 5টা
        page_obj = paginator.get_page(page)

        serializer = CoursesSerializer(page_obj, many=True)

        return Response({
            "msg": "Courses list",
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "data": serializer.data
        })

    # POST (Create)
    def post(self, request):
        serializer = CoursesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Course created",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # PUT (Full Update)
    def put(self, request):
        course_id = request.query_params.get('id')

        if not course_id:
            return Response({"msg": "ID required"}, status=400)

        course = self.get_object(course_id)

        serializer = CoursesSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Course updated",
                "data": serializer.data
            })

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=400)

    # PATCH (Partial Update)
    def patch(self, request):
        course_id = request.query_params.get('id')

        if not course_id:
            return Response({"msg": "ID required"}, status=400)

        course = self.get_object(course_id)

        serializer = CoursesSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Course partially updated",
                "data": serializer.data
            })

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=400)

    # DELETE
    def delete(self, request):
        course_id = request.query_params.get('id')

        if not course_id:
            return Response({"msg": "ID required"}, status=400)

        course = self.get_object(course_id)
        course.delete()

        return Response({
            "msg": "Course deleted"
        }, status=204)    