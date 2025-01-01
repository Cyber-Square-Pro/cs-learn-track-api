from django.urls import path
from api.views import LandingEndPoint, StudentLoginEndPoint, AdminSignInEndPoint

urlpatterns = [
    path('', LandingEndPoint.as_view()),
    path('student/login/', StudentLoginEndPoint.as_view()),
    path('', LandingEndPoint.as_view()),
    path('adminendpoint/login/', AdminSignInEndPoint.as_view())
]
