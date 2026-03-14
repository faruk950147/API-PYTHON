from django.urls import path
from office.views import (
    GeneralView,
    # EmployeeList,
    # EmployeeDetail,
    # EmployeeCreate,
    # EmployeeUpdate,
    # EmployeeDelete
)

urlpatterns = [
    path('', GeneralView.as_view(), name='general'),
    # path('employees/', EmployeeList.as_view(), name='employee_list'),
    # path('employees/<int:id>/', EmployeeDetail.as_view(), name='employee_detail'),
    # path('employees/create/', EmployeeCreate.as_view(), name='employee_create'),
    # path('employees/<int:id>/update/', EmployeeUpdate.as_view(), name='employee_update'),
    # path('employees/<int:id>/delete/', EmployeeDelete.as_view(), name='employee_delete'),
]