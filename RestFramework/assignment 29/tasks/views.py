from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
User = get_user_model()


class TaskListView(LoginRequiredMixin, APIView):
    """
    View to list tasks for the logged-in user.
    """
    template_name = 'tasks/task_list.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

