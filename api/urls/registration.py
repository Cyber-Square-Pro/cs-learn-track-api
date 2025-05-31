from django.urls import path
from api.views import BatchCreationEndPoint, RegisterStudentEndPoint, RegisterTeacherEndPoint

urlpatterns = [
    path('batch/create/', BatchCreationEndPoint.as_view()),
    path('student/register/', RegisterStudentEndPoint.as_view()),
    path('teacher/register/', RegisterTeacherEndPoint.as_view()),
]
