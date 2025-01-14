from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status

class ClearDatabaseView(APIView):
    def post(self, request):
        for model in [StudentData, Batch, Teacher, UserProfile, User]:
            model.objects.all().delete()
        return Response({"message": "All data cleared successfully."}, status=status.HTTP_200_OK)