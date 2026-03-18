from django.urls import path
from office import views

urlpatterns = [
    # API Root
    path("", views.APIRoot.as_view(), name="api-root"),

    # Company
    path('companies/', views.CompanyListView.as_view(), name='company-list'),
    path('companies/create/', views.CompanyListCreateView.as_view(), name='company-create'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('companies/<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company-update'),
    path('companies/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company-delete'),

    # Department
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/create/', views.DepartmentListCreateView.as_view(), name='department-create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department-delete'),

    # Employee
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', views.EmployeeListCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
]