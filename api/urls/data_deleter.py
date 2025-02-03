from django.urls import path
from api.views import DeleteStudent

urlpatterns = [
    path('student/delete/', DeleteStudent.as_view()),
]