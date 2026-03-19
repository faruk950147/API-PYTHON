from rest_framework.views import APIView
from rest_framework import generics, mixins
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
        
class CompanyMixins(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    """
    CompanyMixins provides API endpoints for listing and creating companies.

    This class uses DRF mixins to implement:
        - Listing all companies (GET request)
        - Creating a new company (POST request)

    Attributes:
        queryset (QuerySet): All Company objects from the database.
        serializer_class (Serializer): Serializer used to convert Company objects
            to JSON and validate incoming data.

    Methods:
        get(request, *args, **kwargs):
            Handles GET requests to return a list of all companies.
        post(request, *args, **kwargs):
            Handles POST requests to create a new company.
    """

    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests.

        Returns a list of all companies serialized using
        CompanyHyperlinkedSerializer.
        """
        return self.list(request, *args, **kwargs)  # from ListModelMixin

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests.

        Creates a new company instance using the request data,
        validates it with CompanyHyperlinkedSerializer, and
        returns the serialized new object if successful.
        """
        return self.create(request, *args, **kwargs)  # from CreateModelMixin

