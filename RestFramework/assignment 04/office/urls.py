# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from office.views import CompanyList, DepartmentList, EmployeeList

urlpatterns = [
    # Company endpoints
    path('companies/', CompanyList.as_view(), name='company-list'),
    
    # Department endpoints
    path('departments/', DepartmentList.as_view(), name='department-list'),
    
    # Employee endpoints
    path('employees/', EmployeeList.as_view(), name='employee-list'),
]