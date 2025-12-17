from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class CourseListView(APIView):
    def get(self, request):
        courses = [
            {"id": 1, "name": "Mathematics", "description": "An introduction to mathematical concepts."},
            {"id": 2, "name": "Physics", "description": "Fundamentals of physics and its applications."},
            {"id": 3, "name": "Chemistry", "description": "Basics of chemical reactions and compounds."},
        ]
        return Response(courses)
    def post(self, request):
        return Response({"message": "POST method called"})
    
    def patch(self, request):
        return Response({"message": "PATCH method called"})
    
    def put(self, request):
        return Response({"message": "PUT method called"})
    
    def delete(self, request):
        return Response({"message": "DELETE method called"})
    
    
