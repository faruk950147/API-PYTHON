from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from office.models import Company, Department, Employee
from office.serializers import (
    CompanyHyperlinkedSerializer, 
    DepartmentHyperlinkedSerializer, 
    EmployeeHyperlinkedSerializer
)

# API Root
class APIRoot(APIView):
    """
    API Root: Main entry point for the office app
    """
    def get(self, request, format=None):
        return Response({
            # "companies": reverse("company-list", request=request, format=format),
            # "departments": reverse("department-list", request=request, format=format),
            # "employees": reverse("employee-list", request=request, format=format),
        })