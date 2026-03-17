# urls.py
from django.urls import path
from office.views import (
    CompanyListCreateView,
    CompanyRetrieveUpdateDeleteView,
    DepartmentListCreateView,
    DepartmentRetrieveUpdateDeleteView,
    EmployeeListCreateView,
    EmployeeRetrieveUpdateDeleteView,
)

urlpatterns = [
    # Company URLs
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyRetrieveUpdateDeleteView.as_view(), name='company-detail'),

    # Department URLs
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDeleteView.as_view(), name='department-detail'),

    # Employee URLs
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDeleteView.as_view(), name='employee-detail'),
]