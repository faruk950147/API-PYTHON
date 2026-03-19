from rest_framework.views import APIView
from rest_framework import generics, mixins
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
    API Root endpoint for the Office app.

    Returns hyperlinked URLs for companies, departments, and employees.
    """
    def get(self, request, format=None):
        """
        GET request for API root.

        Args:
            request (Request): The HTTP request object.
            format (str, optional): Format suffix for response. Defaults to None.

        Returns:
            Response: JSON response with hyperlinked API endpoints.
        """
        return Response({
            "companies": reverse("company-list", request=request, format=format),
            "departments": reverse("department-list", request=request, format=format),
            "employees": reverse("employee-list", request=request, format=format),
        })


# Company Views
class CompanyListCreateView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    """
    Provides GET (list) and POST (create) endpoints for Company model.
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

    def get(self, request, *args, **kwargs):
        """Handles GET request: returns a list of all companies."""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handles POST request: creates a new company."""
        return self.create(request, *args, **kwargs)


class CompanyRetrieveUpdateDestroyView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    """
    Provides GET (retrieve), PUT/PATCH (update), and DELETE endpoints for a single Company instance.
    """
    queryset = Company.objects.all()
    serializer_class = CompanyHyperlinkedSerializer

    def get(self, request, *args, **kwargs):
        """Handles GET request: retrieves a single company."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handles PUT request: updates a company completely."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Handles PATCH request: updates a company partially."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handles DELETE request: deletes a company."""
        return self.destroy(request, *args, **kwargs)


# Department Views
class DepartmentListCreateView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
    """
    Provides GET (list) and POST (create) endpoints for Department model.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

    def get(self, request, *args, **kwargs):
        """Handles GET request: returns a list of all departments."""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handles POST request: creates a new department."""
        return self.create(request, *args, **kwargs)


class DepartmentRetrieveUpdateDestroyView(mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.DestroyModelMixin,
                                          generics.GenericAPIView):
    """
    Provides GET (retrieve), PUT/PATCH (update), and DELETE endpoints for a single Department instance.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentHyperlinkedSerializer

    def get(self, request, *args, **kwargs):
        """Handles GET request: retrieves a single department."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handles PUT request: updates a department completely."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Handles PATCH request: updates a department partially."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handles DELETE request: deletes a department."""
        return self.destroy(request, *args, **kwargs)


# Employee Views
class EmployeeListCreateView(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             generics.GenericAPIView):
    """
    Provides GET (list) and POST (create) endpoints for Employee model.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

    def get(self, request, *args, **kwargs):
        """Handles GET request: returns a list of all employees."""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handles POST request: creates a new employee."""
        return self.create(request, *args, **kwargs)


class EmployeeRetrieveUpdateDestroyView(mixins.RetrieveModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin,
                                        generics.GenericAPIView):
    """
    Provides GET (retrieve), PUT/PATCH (update), and DELETE endpoints for a single Employee instance.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeHyperlinkedSerializer

    def get(self, request, *args, **kwargs):
        """Handles GET request: retrieves a single employee."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handles PUT request: updates an employee completely."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Handles PATCH request: updates an employee partially."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handles DELETE request: deletes an employee."""
        return self.destroy(request, *args, **kwargs)