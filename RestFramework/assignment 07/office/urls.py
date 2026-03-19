from django.urls import path
from office.views import (
    APIRoot,
    CompanyListCreateView, CompanyRetrieveUpdateDestroyView,
    DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView,
    EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView
)

urlpatterns = [
    # API Root
    path("", APIRoot.as_view(), name="api-root"),

    # Company URLs
    path("companies/", CompanyListCreateView.as_view(), name="company-list"),
    path("companies/<int:pk>/", CompanyRetrieveUpdateDestroyView.as_view(), name="company-detail"),

    # Department URLs
    path("departments/", DepartmentListCreateView.as_view(), name="department-list"),
    path("departments/<int:pk>/", DepartmentRetrieveUpdateDestroyView.as_view(), name="department-detail"),

    # Employee URLs
    path("employees/", EmployeeListCreateView.as_view(), name="employee-list"),
    path("employees/<int:pk>/", EmployeeRetrieveUpdateDestroyView.as_view(), name="employee-detail"),
]