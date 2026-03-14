from django.urls import path
from office.views import (
    CompanyList,
    DepartmentList,
    EmployeeList
)

urlpatterns = [
    path('companies/', CompanyList.as_view()),
    path('departments/', DepartmentList.as_view()),
    path('employees/', EmployeeList.as_view()),
]