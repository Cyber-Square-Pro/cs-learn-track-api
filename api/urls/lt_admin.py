from django.urls import path
from api.views import LandingEndPoint, StudentLoginEndPoint, BatchCreationEndPoint, RegisterStudentEndPoint

urlpatterns = [
    path('', LandingEndPoint.as_view()),
    path('student/login/', StudentLoginEndPoint.as_view()),
    path('batch/create/', BatchCreationEndPoint.as_view()),
    path('student/register/', RegisterStudentEndPoint.as_view())
]
