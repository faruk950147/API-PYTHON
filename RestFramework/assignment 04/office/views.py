from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from office.models import (
    Company,
    Department,
    Employee
)
from office.serializers import (
    CompanyHyperlinkedSerializer, 
    DepartmentHyperlinkedSerializer, 
    EmployeeHyperlinkedSerializer
)

# Companies Api
class CompanyList(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanyHyperlinkedSerializer(companies, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CompanyHyperlinkedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Department API
class DepartmentList(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentHyperlinkedSerializer(departments, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DepartmentHyperlinkedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Employee API
class EmployeeList(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeHyperlinkedSerializer(employees, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EmployeeHyperlinkedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)