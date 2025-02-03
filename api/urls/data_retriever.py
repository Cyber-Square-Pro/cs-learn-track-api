from django.urls import path
from api.views import ListBatchEndPoint, CheckUserTypeEndPoint, GetTeacherData, GetStudentData, GetTeacherDashboardDetails, GetStudentList

urlpatterns = [
    path('batch/list/', ListBatchEndPoint.as_view()),
    path('CheckUserTypeEndPoint/', CheckUserTypeEndPoint.as_view()),
    path('teacher/data/', GetTeacherData.as_view()),
    path('student/data/', GetStudentData.as_view()),
    path('teacher/dashboard/', GetTeacherDashboardDetails.as_view()),
    path('batch/listStudents/', GetStudentList.as_view()),
]
