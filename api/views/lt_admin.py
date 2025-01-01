from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from api.models import AdminData, StudentData
from api.serializer import AdminDataSerializer, StudentLoginSerializer
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

class StudentLoginEndPoint(APIView):
    """
    API endpoint for student login.

    This endpoint handles POST requests for student login. It validates the provided
    student credentials and checks if the student exists in the database. 

    Methods:
        post(request): 
            Handles the login process for students. It expects a JSON payload with 
            'studentID' and 'studentPassword'. If the credentials are valid, it returns 
            a success message; otherwise, it returns an appropriate error message.

    Responses:
        - 200 OK: If the student is successfully logged in.
        - 400 Bad Request: If the provided data is invalid, the student does not exist, 
          or the password is incorrect.
    """
    def post(self, request):
        serializer = StudentLoginSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "status":  status.HTTP_400_BAD_REQUEST})
        student_data = serializer.validated_data

        if not StudentData.objects.filter(studentID = student_data["studentID"]).exists():
            return Response({"message": "Student  does not exist", "status":  status.HTTP_400_BAD_REQUEST})
        
        if StudentData.objects.get(studentID = student_data["studentID"]).studentPassword == student_data["studentPassword"]:
            return Response({"message": "Student logged in successfully", "status":  status.HTTP_200_OK})
        else:
            return Response({"message": "Invalid password", "status":  status.HTTP_400_BAD_REQUEST})