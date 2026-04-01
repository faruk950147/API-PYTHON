from django.urls import path
from account.views import (
    CustomAuthToken
)

urlpatterns = [  
    path('get-token/', CustomAuthToken.as_view(), name='get-token'),
]