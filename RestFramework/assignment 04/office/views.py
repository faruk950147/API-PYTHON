from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from office.models import Company, Department, Employee
from office.serializers import CompanyHyperlinkedSerializer, DepartmentHyperlinkedSerializer, EmployeeHyperlinkedSerializer

# ----------------- Company API ----------------- #
class CompanyList(APIView):
    """
    API view to list all companies or create a new company.
    """
    def get(self, request):
        """
        GET method to retrieve all companies.
        Returns a list of companies with hyperlinked relationships.
        """
        companies = Company.objects.all()
        serializer = CompanyHyperlinkedSerializer(companies, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        """
        POST method to create a new company.
        Expects company data in the request body.
        """
        serializer = CompanyHyperlinkedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompaniesDetail(APIView):
    """
    API view to retrieve, update, or delete a single company by its ID.
    """
    def get_object(self, pk):
        """
        Helper method to retrieve a company by primary key (pk).
        Raises Http404 if the company does not exist.
        """
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        GET method to retrieve a specific company by ID.
        """
        company = self.get_object(pk)
        serializer = CompanyHyperlinkedSerializer(company, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        PUT method to fully update a specific company by ID.
        """
        company = self.get_object(pk)
        serializer = CompanyHyperlinkedSerializer(company, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        DELETE method to remove a specific company by ID.
        """
        company = self.get_object(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------------- Department API ----------------- #
class DepartmentList(APIView):
    """
    API view to list all departments or create a new department.
    """
    def get(self, request):
        """
        GET method to retrieve all departments.
        Returns a list of departments with hyperlinked relationships.
        """
        departments = Department.objects.all()
        serializer = DepartmentHyperlinkedSerializer(departments, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        """
        POST method to create a new department.
        Expects department data in the request body.
        """
        serializer = DepartmentHyperlinkedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentDetail(APIView):
    """
    API view to retrieve, update, or delete a single department by its ID.
    """
    def get_object(self, pk):
        """
        Helper method to retrieve a department by primary key (pk).
        Raises Http404 if the department does not exist.
        """
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        GET method to retrieve a specific department by ID.
        """
        department = self.get_object(pk)
        serializer = DepartmentHyperlinkedSerializer(department, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        PUT method to fully update a specific department by ID.
        """
        department = self.get_object(pk)
        serializer = DepartmentHyperlinkedSerializer(department, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        DELETE method to remove a specific department by ID.
        """
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------------- Employee API ----------------- #
class EmployeeList(APIView):
    """
    API view to list all employees or create a new employee.
    """
    def get(self, request):
        """
        GET method to retrieve all employees.
        Returns a list of employees with hyperlinked relationships.
        """
        employees = Employee.objects.all()
        serializer = EmployeeHyperlinkedSerializer(employees, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        """
        POST method to create a new employee.
        Expects employee data in the request body.
        """
        serializer = EmployeeHyperlinkedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    """
    API view to retrieve, update, or delete a single employee by its ID.
    """
    def get_object(self, pk):
        """
        Helper method to retrieve an employee by primary key (pk).
        Raises Http404 if the employee does not exist.
        """
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        GET method to retrieve a specific employee by ID.
        """
        employee = self.get_object(pk)
        serializer = EmployeeHyperlinkedSerializer(employee, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        PUT method to fully update a specific employee by ID.
        """
        employee = self.get_object(pk)
        serializer = EmployeeHyperlinkedSerializer(employee, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        DELETE method to remove a specific employee by ID.
        """
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)