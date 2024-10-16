from django.urls import path
from api.views import LandingEndPoint

urlpatterns = [
    path('', LandingEndPoint.as_view())
]
