# urls.py
from django.urls import path
from office.views import (
    CompanyList, CompaniesDetail,
    DepartmentList, DepartmentDetail,
    EmployeeList, EmployeeDetail
)

urlpatterns = [
    # Company endpoints
    path('companies/', CompanyList.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompaniesDetail.as_view(), name='company-detail'),

    # Department endpoints
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),

    # Employee endpoints
    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetail.as_view(), name='employee-detail'),
]