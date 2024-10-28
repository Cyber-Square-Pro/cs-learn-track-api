from django.urls import path
from api.views import AdminSignInEndPoint, LandingEndPoint

urlpatterns = [
    path('', LandingEndPoint.as_view()),
    path('admin/login/', AdminSignInEndPoint.as_view())
]
