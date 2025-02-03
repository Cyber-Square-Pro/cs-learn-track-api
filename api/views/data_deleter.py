from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.permissions import isTeacher, isStudent
from rest_framework_simplejwt.authentication import JWTAuthentication

class DeleteStudent(APIView):
    """
    API endpoint to delete a student.

    This endpoint handles POST requests to delete a student by changing their account status to false
    and reassigning roll numbers in the class.

    Methods:
        post(request): 
            Handles the student deletion process. It expects a JSON payload with the student's admission number.
            If the student is found, it updates the account status and reassigns roll numbers.

    Responses:
        - 200 OK: If the student is successfully deleted.
        - 400 Bad Request: If the provided data is invalid or the student does not exist.

    Created by: Yash Raj on 11/01/2025
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        admission_no = request.data.get("admissionNo")
        if not admission_no:
            return Response({"message": "Admission number is required", "status": status.HTTP_400_BAD_REQUEST})

        try:
            student = StudentData.objects.get(admissionNo=admission_no)
        except StudentData.DoesNotExist:
            return Response({"message": "Student does not exist", "status": status.HTTP_400_BAD_REQUEST})

        # Reassign roll numbers
        student.accountStatus = False
        student.rollNo = 0
        student.save()

        batch = student.batch

        students_in_batch = StudentData.objects.filter(batch=batch, accountStatus=True).order_by('studentName')
        for index, student in enumerate(students_in_batch, start=1):
            student.rollNo = index
            student.save()

        return Response({"message": "Student deleted successfully", "status": status.HTTP_200_OK})

