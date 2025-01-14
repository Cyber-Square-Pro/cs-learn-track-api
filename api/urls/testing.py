from django.urls import path
from api.views import ClearDatabaseView

urlpatterns = [
    path('database/clear/', ClearDatabaseView.as_view())
]