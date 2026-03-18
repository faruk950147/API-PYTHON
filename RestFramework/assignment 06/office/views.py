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

# API Root
class APIRoot(APIView):
    """
    API Root: Main entry point for the office app
    """
    def get(self, request, format=None):
        return Response({
            "companies": reverse("company-list", request=request, format=format),
            "departments": reverse("department-list", request=request, format=format),
            "employees": reverse("employee-list", request=request, format=format),
        })


# Company Views
class CompanyListCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyUpdateView(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyDeleteView(generics.DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer


# Department Views
class DepartmentListCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentUpdateView(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentDeleteView(generics.DestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer


# Employee Views
class EmployeeListCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeDeleteView(generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer