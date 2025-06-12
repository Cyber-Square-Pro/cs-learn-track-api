from django.urls import path
from api.views import BatchCreationEndPoint, RegisterStudentEndPoint, RegisterTeacherEndPoint, AddFaceEncodingEndPoint

urlpatterns = [
    path('batch/create/', BatchCreationEndPoint.as_view()),
    path('student/register/', RegisterStudentEndPoint.as_view()),
    path('teacher/register/', RegisterTeacherEndPoint.as_view()),
    path('add_pfp_and_face_encoding/', AddFaceEncodingEndPoint.as_view()),
]
