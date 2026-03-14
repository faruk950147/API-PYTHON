from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from office.models import  Company, Department, Employee
from office.serializers import CompanyHyperlinkedSerializer, DepartmentHyperlinkedSerializer, EmployeeHyperlinkedSerializer

class GeneralView(APIView):
    def get(self, request):
        return Response({"status": "success"})
    
