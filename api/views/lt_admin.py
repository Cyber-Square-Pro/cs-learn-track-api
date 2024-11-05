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
    """
    API endpoint for admin sign-in.

    This endpoint allows an admin to log in by providing their username and password.
    It validates the input data and checks if the admin exists in the database. If the 
    admin exists, it verifies the password. Depending on the outcome of these checks, 
    it returns an appropriate response.

    Methods:
        post(request): Handles POST requests for admin sign-in.
            - Expects a JSON payload with 'username' and 'password'.
            - Returns:
                - 200 OK if login is successful.
                - 400 Bad Request if the data is invalid or if the admin does not exist.
                - 400 Bad Request if the password is incorrect.
    """
    def post(self, request):
        serializer = AdminDataSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "status":  status.HTTP_400_BAD_REQUEST})
        admin_data = serializer.validated_data

        if not AdminData.objects.filter(username = admin_data["username"]).exists():
            return Response({"message": "Admin  does not exist", "status":  status.HTTP_400_BAD_REQUEST})
        
        if AdminData.objects.get(username = admin_data["username"]).password == admin_data["password"]:
            return Response({"message": "Admin logged in successfully", "status":  status.HTTP_200_OK})
        else:
            return Response({"message": "Invalid password", "status":  status.HTTP_400_BAD_REQUEST})

