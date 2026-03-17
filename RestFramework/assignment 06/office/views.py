# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from office.models import Company, Department, Employee
from office.serializers import (
    CompanyHyperlinkedSerializer, 
    DepartmentHyperlinkedSerializer, 
    EmployeeHyperlinkedSerializer
)

# Company Views
class CompanyListCreateView(generics.ListCreateAPIView):
    ''' Get all objects for get request
        Create objects for post request'''
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

class CompanyRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

# Department Views
class DepartmentListCreateView(generics.ListCreateAPIView):
    ''' Get all objects for get request
        Create objects for post request'''
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

class DepartmentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

# Employee Views
class EmployeeListCreateView(generics.ListCreateAPIView):
    ''' Get all objects for get request
        Create objects for post request'''
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer