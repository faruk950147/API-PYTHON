from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class GeneralView(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the Office API",
            # "version": "1.0.0",
            # "status": "running",
            # "base_url": "http://127.0.0.1:8000/",
            # "endpoints": [
            #     "/employees/",
            #     "/employees/<id>/",
            #     "/employees/create/",
            #     "/employees/<id>/update/",
            #     "/employees/<id>/delete/",
            # ]
        })