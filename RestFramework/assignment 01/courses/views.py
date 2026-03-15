from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import Courses
from courses.serializers import CoursesSerializer


class EndPointsListView(APIView):
    def get(self, request):
        return Response({
            'status': 'success',
            'endPoints': [
                'http://127.0.0.1:8000/api/courses/'
            ]
        })


class CoursesView(APIView):
    def get_object(self, request):
        course_id = request.data.get('id')
        if not course_id:
            return None
        try:
            return Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
             raise Http404

    def get(self, request):
        courses = Courses.objects.all()
        serializer = CoursesSerializer(courses, many=True)
        return Response({
            "msg": "Courses retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
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
        course = self.get_object(request)
        if not course:
            return Response({"msg": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        course.delete()
        return Response({
            "msg": "Course deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)