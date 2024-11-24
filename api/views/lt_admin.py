from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from api.models import StudentData, Batch
from api.serializer import StudentLoginSerializer, BatchCreationSerializer
from rest_framework import status

class LandingEndPoint(APIView):
    def get(self,request):
        return HttpResponse('<h1 align="center" style="margin-top:200px">Welcome Onboard!..</h1>')


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

class BatchCreationEndPoint(APIView):
    def post(self, request):
        serializer = BatchCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})
        
        serializer.save()
        return Response({"message": "Batch created successfully", "status": status.HTTP_201_CREATED})