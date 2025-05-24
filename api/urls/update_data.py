from api.views import UpdateStudentData, UpdateBatchData
from django.urls import path

urlpatterns = [
    path('student/update/', UpdateStudentData.as_view(), name='update_student_data'),
    path('batch/update/', UpdateBatchData.as_view(), name='update_batch_data'),
]