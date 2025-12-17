from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from account.views import SignupView, SignInView, SignOutView
urlpatterns = [
    path('sign_up/', csrf_exempt(SignupView.as_view()), name='sign_up'),
    path('sign_in/', csrf_exempt(SignInView.as_view()), name='sign_in'),
    path('sign_out/', csrf_exempt(SignOutView.as_view()), name='sign_out'),
]