from django.urls import path
from api.views import GetStudentList

url_patterns = [
    path('batch/list_students/', GetStudentList.as_view()),
]