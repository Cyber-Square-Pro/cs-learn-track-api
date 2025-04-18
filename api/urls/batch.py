from django.urls import path
from api.views import GetBatchStudentList, RemoveStudent, GetTeacherStudentList

url_patterns = [
    path('batch/list_batch_students/', GetBatchStudentList.as_view()),
    path('batch/remove_student/', RemoveStudent.as_view()),
    path('batch/teacher_student_list/', GetTeacherStudentList.as_view()),
]