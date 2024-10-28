from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import AdminAccess
from .serializer import AdminAccessSerializer

class AdminSignInEndPoint(APIView):
    def post(self, request):
        if not AdminAccess.objects.filter(username = request.data["username"]).exists():
            return Response({"message": "Admin  does not exist", "status":  status.HTTP_400_BAD_REQUEST})
        
        serializer = AdminAccessSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "status":  status.HTTP_400_BAD_REQUEST})
        
        if AdminAccess.objects.get(username = request.data["username"]).password == request.data["password"]:
            return Response({"message": "Admin logged in successfully", "status":  status.HTTP_200_OK})
        else:
            return Response({"message": "Invalid password", "status":  status.HTTP_400_BAD_REQUEST})


