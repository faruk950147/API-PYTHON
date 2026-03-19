from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from office.models import Company, Department, Employee
from office.serializers import (
    CompanyHyperlinkedSerializer, 
    DepartmentHyperlinkedSerializer, 
    EmployeeHyperlinkedSerializer
)

# =============================
# API Root
# =============================
class APIRoot(APIView):
    """
    API Root: Main entry point for the office app.
    
    Returns hyperlinks to all main endpoints:
    - companies
    - departments
    - employees
    """
    def get(self, request, format=None):
        return Response({
            "companies": reverse("company-list", request=request, format=format),
            "departments": reverse("department-list", request=request, format=format),
            "employees": reverse("employee-list", request=request, format=format),
        })

# =============================
# Company Views
# =============================
class CompanyListCreateView(generics.CreateAPIView):
    """
    Create a new Company.
    URL: POST /companies/
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyListView(generics.ListAPIView):
    """
    List all Companies.
    URL: GET /companies/
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single Company by ID.
    URL: GET /companies/{id}/
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyUpdateView(generics.UpdateAPIView):
    """
    Update an existing Company by ID.
    URL: PUT /companies/{id}/
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyDeleteView(generics.DestroyAPIView):
    """
    Delete a Company by ID.
    URL: DELETE /companies/{id}/
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

# =============================
# Department Views
# =============================
class DepartmentListCreateView(generics.CreateAPIView):
    """
    Create a new Department.
    URL: POST /departments/
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentListView(generics.ListAPIView):
    """
    List all Departments.
    URL: GET /departments/
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single Department by ID.
    URL: GET /departments/{id}/
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentUpdateView(generics.UpdateAPIView):
    """
    Update an existing Department by ID.
    URL: PUT /departments/{id}/
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentDeleteView(generics.DestroyAPIView):
    """
    Delete a Department by ID.
    URL: DELETE /departments/{id}/
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

# =============================
# Employee Views
# =============================
class EmployeeListCreateView(generics.CreateAPIView):
    """
    Create a new Employee.
    URL: POST /employees/
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeListView(generics.ListAPIView):
    """
    List all Employees.
    URL: GET /employees/
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single Employee by ID.
    URL: GET /employees/{id}/
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeUpdateView(generics.UpdateAPIView):
    """
    Update an existing Employee by ID.
    URL: PUT /employees/{id}/
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeDeleteView(generics.DestroyAPIView):
    """
    Delete an Employee by ID.
    URL: DELETE /employees/{id}/
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer