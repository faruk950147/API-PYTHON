from rest_framework.routers import DefaultRouter
from admission.views import StudentViewSet, GeneralView
from django.urls import path

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', GeneralView.as_view(), name='general'),
]

urlpatterns += router.urls