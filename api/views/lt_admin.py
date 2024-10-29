from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from api.models import StudentData
from api.serializer import StudentLoginSerializer
from rest_framework import status

class LandingEndPoint(APIView):
    def get(self,request):
        return HttpResponse('<h1 align="center" style="margin-top:200px">Welcome Onboard!..</h1>')


class StudentLoginEndPoint(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)