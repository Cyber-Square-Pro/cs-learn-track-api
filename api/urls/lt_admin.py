from django.urls import path
from api.views import LandingEndPoint
from api.views import AdminSignInEndPoint

urlpatterns = [
    path('', LandingEndPoint.as_view()),
    path('adminendpoint/login/', AdminSignInEndPoint.as_view())
]
