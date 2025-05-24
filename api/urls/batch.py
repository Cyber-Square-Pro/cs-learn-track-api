from django.urls import path
from api.views import GetBatchStudentList, RemoveStudent, GetTeacherStudentList, CreateSession, GetBatchSessions

url_patterns = [
    path('batch/list_batch_students/', GetBatchStudentList.as_view()),
    path('batch/remove_student/', RemoveStudent.as_view()),
    path('batch/teacher_student_list/', GetTeacherStudentList.as_view()),
    path('batch/create_session/', CreateSession.as_view()),
    path('batch/get_batch_sessions/', GetBatchSessions.as_view()),
]