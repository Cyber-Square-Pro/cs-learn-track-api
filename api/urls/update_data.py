from api.views import UpdateStudentData, UpdateBatchData, UpdateSessionData, UpdateTeacherData
from django.urls import path

urlpatterns = [
    path('student/update/', UpdateStudentData.as_view(), name='update_student_data'),
    path('batch/update/', UpdateBatchData.as_view(), name='update_batch_data'),
    path('session/update/', UpdateSessionData.as_view(), name='update_session_data'),
    path('teacher/update/', UpdateTeacherData.as_view(), name='update_teacher_data'),
]