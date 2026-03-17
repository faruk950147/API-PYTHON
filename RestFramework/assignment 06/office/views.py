from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from office.models import Company, Department, Employee
from office.serializers import CompanyHyperlinkedSerializer, DepartmentHyperlinkedSerializer, EmployeeHyperlinkedSerializer

# Company API
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

class CompaniesDetail(APIView):
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        company = self.get_object(pk)
        if not company:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyHyperlinkedSerializer(company, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_object(pk)
        if not company:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyHyperlinkedSerializer(company, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = self.get_object(pk)
        if not company:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class DepartmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentHyperlinkedSerializer(department, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentHyperlinkedSerializer(department, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeHyperlinkedSerializer(employee, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeHyperlinkedSerializer(employee, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)