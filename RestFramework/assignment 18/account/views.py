from urllib import request

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from account.mixing import LoginRequiredMixin, LogoutRequiredMixin

User = get_user_model()


@method_decorator(never_cache, name='dispatch')
class SignupView(LogoutRequiredMixin, View):
    def get(self, request):
        messages.info(request, 'Please sign up to continue.')
        return render(request, 'account/signup.html')

    def post(self, request):
        messages.success(request, 'Account signed up successfully. Please log in.')
        return redirect('login')


@method_decorator(never_cache, name='dispatch')
class LoginView(LogoutRequiredMixin, View):
    def get(self, request):
        messages.info(request, 'Please log in to continue.')
        return render(request, 'account/login.html')

    def post(self, request):
        messages.success(request, 'You have been logged in successfully.')   
        return redirect('home')


@method_decorator(never_cache, name='dispatch')
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')