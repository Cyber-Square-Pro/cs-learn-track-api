from api.views import UpdateStudentData
from django.urls import path

urlpatterns = [
    path('student/update/', UpdateStudentData.as_view(), name='update_student_data'),
]