from django.urls import path
from api.views import ClearDatabaseView, TestView

urlpatterns = [
    path('database/clear/', ClearDatabaseView.as_view()),
    path('test/', TestView.as_view())
]