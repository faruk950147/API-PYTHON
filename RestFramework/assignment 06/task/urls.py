from django.urls import path
from task.views import(
    List
)
urlpatterns = [
    path('', List, name='List')
]
