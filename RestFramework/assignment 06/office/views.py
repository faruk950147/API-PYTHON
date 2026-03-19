# views.py
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
    API Root: Main entry point for the Office app.
    
    Provides hyperlinks to the main resources: companies, departments, and employees.
    """
    def get(self, request, format=None):
        """
        GET method to return the root API links.
        """
        return Response({
            "companies": reverse("company-list", request=request, format=format),
            "departments": reverse("department-list", request=request, format=format),
            "employees": reverse("employee-list", request=request, format=format),
        })

# Company Views 
class CompanyListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView for Company:
    
    GET  - List all companies.
    POST - Create a new company.
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for Company:
    
    GET    - Retrieve a company by ID.
    PUT    - Update a company completely.
    PATCH  - Update a company partially.
    DELETE - Delete a company by ID.
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

# Department Views
class DepartmentListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView for Department:
    
    GET  - List all departments.
    POST - Create a new department.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for Department:
    
    GET    - Retrieve a department by ID.
    PUT    - Update a department completely.
    PATCH  - Update a department partially.
    DELETE - Delete a department by ID.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

# Employee Views
class EmployeeListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView for Employee:
    
    GET  - List all employees.
    POST - Create a new employee.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for Employee:
    
    GET    - Retrieve an employee by ID.
    PUT    - Update an employee completely.
    PATCH  - Update an employee partially.
    DELETE - Delete an employee by ID.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer