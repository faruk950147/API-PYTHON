from django.urls import path
from tasks.views import TaskListView
urlpatterns = [
    # Define your URL patterns here 
    path('', TaskListView.as_view(), name='task_list'),
]
