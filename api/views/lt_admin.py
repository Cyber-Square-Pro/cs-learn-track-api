from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from api.models import Studentdata
from api.serializer import StudentLoginSerializer
from rest_framework import status

class LandingEndPoint(APIView):
    def get(self,request):
        return HttpResponse('<h1 align="center" style="margin-top:200px">Welcome Onboard!..</h1>')


class StudentLoginEndPoint(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "status":  status.HTTP_400_BAD_REQUEST})
        student_data = serializer.validated_data

        if not Studentdata.objects.filter(studentID = student_data["studentID"]).exists():
            return Response({"message": "Student  does not exist", "status":  status.HTTP_400_BAD_REQUEST})
        
        if Studentdata.objects.get(studentID = student_data["studentID"]).studentPassword == student_data["studentPassword"]:
            return Response({"message": "Student logged in successfully", "status":  status.HTTP_200_OK})
        else:
            return Response({"message": "Invalid password", "status":  status.HTTP_400_BAD_REQUEST})