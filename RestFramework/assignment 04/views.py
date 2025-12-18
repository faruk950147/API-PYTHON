from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from info.models import Admission
from info.serializers import AdmissionSerializer


class StudentInfoView(APIView):
