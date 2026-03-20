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
        # PATCH method to partially update an existing course.
        # Expects the course ID in request data and the fields to update.
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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Courses
from .serializers import CoursesSerializer
from .pagination import CoursePagination
from django.db.models import Q

class CoursesView(APIView):

    # GET (single + all + search + pagination)
    def get(self, request):
        course_id = request.query_params.get('id')
        search = request.query_params.get('search')

        # Single Course
        if course_id:
            course = get_object_or_404(Courses, id=course_id)
            serializer = CoursesSerializer(course)
            return Response({
                "msg": "Single course",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        # All Courses
        courses = Courses.objects.all()

        # Search
        if search:
            courses = courses.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Pagination
        paginator = CoursePagination()
        result_page = paginator.paginate_queryset(courses, request)
        serializer = CoursesSerializer(result_page, many=True)

        return paginator.get_paginated_response({
            "msg": "Courses list",
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
            return Response({"msg": "ID required"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Courses, id=course_id)
        serializer = CoursesSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Course updated",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # PATCH (Partial Update)
    def patch(self, request):
        course_id = request.query_params.get('id')
        if not course_id:
            return Response({"msg": "ID required"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Courses, id=course_id)
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

    # DELETE
    def delete(self, request):
        course_id = request.query_params.get('id')
        if not course_id:
            return Response({"msg": "ID required"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Courses, id=course_id)
        course.delete()
        return Response({"msg": "Course deleted"}, status=status.HTTP_200_OK)

'''
      
'''      
from rest_framework import generics, status, filters
from rest_framework.response import Response
from .models import Courses
from .serializers import CoursesSerializer
from rest_framework.pagination import PageNumberPagination

# Custom Pagination
class CoursesPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 50

# Full CRUD View
class CoursesView(generics.GenericAPIView):
    serializer_class = CoursesSerializer
    queryset = Courses.objects.all()
    pagination_class = CoursesPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']  # Searchable fields

    # GET: single / all / search / pagination
    def get(self, request):
        course_id = request.query_params.get('id')

        if course_id:
            course = generics.get_object_or_404(Courses, id=course_id)
            serializer = self.get_serializer(course)
            return Response({"msg": "Single course", "data": serializer.data})

        courses = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(courses, many=True)
        return Response({"msg": "Courses list", "data": serializer.data})

    # POST: Create
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Course created", "data": serializer.data}, status=status.HTTP_201_CREATED)

    # PUT: Full update
    def put(self, request):
        course_id = request.query_params.get('id')
        if not course_id:
            return Response({"msg": "ID required"}, status=status.HTTP_400_BAD_REQUEST)
        course = generics.get_object_or_404(Courses, id=course_id)
        serializer = self.get_serializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Course updated", "data": serializer.data})

    # PATCH: Partial update
    def patch(self, request):
        course_id = request.query_params.get('id')
        if not course_id:
            return Response({"msg": "ID required"}, status=status.HTTP_400_BAD_REQUEST)
        course = generics.get_object_or_404(Courses, id=course_id)
        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Course partially updated", "data": serializer.data})

    # DELETE
    def delete(self, request):
        course_id = request.query_params.get('id')
        if not course_id:
            return Response({"msg": "ID required"}, status=status.HTTP_400_BAD_REQUEST)
        course = generics.get_object_or_404(Courses, id=course_id)
        course.delete()
        return Response({"msg": "Course deleted"})        
'''
