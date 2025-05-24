from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.permissions import isTeacher, isStudent
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.db.models import Q

class UpdateStudentData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher | isStudent]

    def post(self, request):
        data = request.data
        admission_no = data.get('admission_no')
        if not admission_no:
            return Response({"error": "admission_no is required"}, status=status.HTTP_400_BAD_REQUEST)
        student = StudentData.objects.filter(admissionNo=admission_no).first()

        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentRegistrationSerializer(student, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateBatchData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        data = request.data
        batch_id = data.get('batch_id')
        if not batch_id:
            return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        batch = Batch.objects.filter(id=batch_id).first()

        if not batch:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BatchSerializer(batch, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)