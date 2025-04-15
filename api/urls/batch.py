from django.urls import path
from api.views import GetStudentList, RemoveStudent

url_patterns = [
    path('batch/list_students/', GetStudentList.as_view()),
    path('batch/remove_student/', RemoveStudent.as_view()),
]