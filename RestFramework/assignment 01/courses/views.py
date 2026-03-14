from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import Courses
from courses.serializers import CoursesSerializer


class EndPointsListView(APIView):
    def get(self, request):
        return Response({
            'status': 'success'
        })


class CoursesView(APIView):
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
                "msg": "Courses created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        courses = get_object_or_404(Courses, id=request.data.get('id'))

        serializer = CoursesSerializer(courses, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Courses updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        courses = get_object_or_404(Courses, id=request.data.get('id'))

        serializer = CoursesSerializer(courses, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Courses partially updated",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "msg": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        courses = get_object_or_404(Courses, id=request.data.get('id'))

        courses.delete()

        return Response({
            "msg": "Courses deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    