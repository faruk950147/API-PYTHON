from django.urls import path
from api.views import (
    ApiOverview, TaskSaved, TaskList, TaskDetails, TaskUpdated, TaskDeleted
)
urlpatterns = [
    path('', ApiOverview, name='ApiOverview'),
    path('TaskSaved/', TaskSaved, name='TaskSaved'),
    path('TaskList/', TaskList, name='TaskList'),
    path('TaskDetails/<int:id>/', TaskDetails, name='TaskDetails'),
    path('TaskUpdated/<int:id>/', TaskUpdated, name='TaskUpdated'),
    path('TaskDeleted/<int:id>/', TaskDeleted, name='TaskDeleted'),
]
