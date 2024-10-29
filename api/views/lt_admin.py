from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from api.models import AdminData
from api.serializer import AdminDataSerializer
from rest_framework import status


class LandingEndPoint(APIView):
    def get(self,request):
        return HttpResponse('<h1 align="center" style="margin-top:200px">Welcome Onboard!..</h1>')


class AdminSignInEndPoint(APIView):
    def post(self, request):
        if not AdminData.objects.filter(username = request.data["username"]).exists():
            return Response({"message": "Admin  does not exist", "status":  status.HTTP_400_BAD_REQUEST})
        
        serializer = AdminDataSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "status":  status.HTTP_400_BAD_REQUEST})
        
        if AdminData.objects.get(username = request.data["username"]).password == request.data["password"]:
            return Response({"message": "Admin logged in successfully", "status":  status.HTTP_200_OK})
        else:
            return Response({"message": "Invalid password", "status":  status.HTTP_400_BAD_REQUEST})

