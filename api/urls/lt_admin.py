from django.urls import path
from api.views import *

urlpatterns = [
    path('', LandingEndPoint.as_view()),
    path('student/login/', StudentLoginEndPoint.as_view()),
    path('batch/create/', BatchCreationEndPoint.as_view()),
    path('student/register/', RegisterStudentEndPoint.as_view()),
    path('teacher/register/', RegisterTeacherEndPoint.as_view()),
    path('teacher/login/', TeacherLoginEndPoint.as_view()),
    path('AuthTest/', AuthTest.as_view()),
    path('adminendpoint/login/', AdminSignInEndPoint.as_view())
]
