from django.urls import path
from office.views import (
    APIRoot,
    CompanyListCreateView,
    CompanyRetrieveUpdateDeleteView,
    DepartmentListCreateView,
    DepartmentRetrieveUpdateDeleteView,
    EmployeeListCreateView,
    EmployeeRetrieveUpdateDeleteView,
)

urlpatterns = [
    # API Root
    path("", APIRoot.as_view(), name="api-root"),
    
    # Company URLs
    path('companies/', CompanyListCreateView.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyRetrieveUpdateDeleteView.as_view(), name='company-detail'),

    # Department URLs
    path('departments/', DepartmentListCreateView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDeleteView.as_view(), name='department-detail'),

    # Employee URLs
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDeleteView.as_view(), name='employee-detail'),
]