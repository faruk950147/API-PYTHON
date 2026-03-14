from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class CourseListView(APIView):
    def get(self, request):
        admission = [
            {"id": 1, "name": "John Doe", "roll": 123456, "cgpa": 3.5},
            {"id": 2, "name": "Jane Smith", "roll": 123457, "cgpa": 3.8},
            {"id": 3, "name": "Jim Beam", "roll": 123458, "cgpa": 3.2},
        ]
        return Response(admission)
    def post(self, request):
        return Response({"message": "POST method called"})
    
    def patch(self, request):
        return Response({"message": "PATCH method called"})
    
    def put(self, request):
        return Response({"message": "PUT method called"})
    
    def delete(self, request):
        return Response({"message": "DELETE method called"})
    
    
