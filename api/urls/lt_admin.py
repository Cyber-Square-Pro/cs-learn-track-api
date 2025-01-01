from django.urls import path
from api.views import LandingEndPoint, StudentLoginEndPoint

urlpatterns = [
    path('', LandingEndPoint.as_view()),
    path('student/login/', StudentLoginEndPoint.as_view())
]
