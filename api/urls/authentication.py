from django.urls import path
from api.views import StudentLoginEndPoint, TeacherLoginEndPoint, AdminSignInEndPoint, LogoutEndPoint, RegenerateAccessToken, AddFaceEncodingEndPoint, LoginFaceEndPoint

urlpatterns = [
    path('student/login/', StudentLoginEndPoint.as_view()),
    path('teacher/login/', TeacherLoginEndPoint.as_view()),
    path('adminendpoint/login/', AdminSignInEndPoint.as_view()),
    path('logout/', LogoutEndPoint.as_view()),
    path('token/refresh/', RegenerateAccessToken.as_view()),
    path('add_face_encoding/', AddFaceEncodingEndPoint.as_view()),
    path('student/login_face/', LoginFaceEndPoint.as_view()),
]
