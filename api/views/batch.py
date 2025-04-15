from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.permissions import isTeacher, isStudent
from rest_framework_simplejwt.authentication import JWTAuthentication

class GetStudentList(APIView):
    """
    API endpoint to retrieve the list of students in a given batch.

    This endpoint handles POST requests and returns the batch name along with a list of students.

    Methods:
        post(request): 
            Expects 'batch_id' in the request data and returns the batch name and its students.

    Responses:
        - 200 OK: If the batch is found and students are returned.
        - 400 Bad Request: If 'batch_id' is not provided.
        - 404 Not Found: If the batch does not exist.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 15/04/2025
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        batch_id = request.data.get('batch_id')
        if not batch_id:
            return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            batch = Batch.objects.get(id=batch_id)
            students = StudentData.objects.filter(batch=batch).order_by('rollNo')
            data = {
                "batch": batch.batchName,
                "students": [
                    {
                        "name": student.studentName,
                        "rollNo": student.rollNo,
                        "admissionNo": student.admissionNo,
                    } for student in students
                ]
            }
            return Response(data, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)

class RemoveStudent(APIView):
    """
    API endpoint to remove a student from a batch.

    This endpoint handles POST requests and removes a student from the specified batch.

    Methods:
        post(request): 
            Expects 'admissionNo' in the request data and removes the student.

    Responses:
        - 200 OK: If the student is successfully removed.
        - 400 Bad Request: If 'student_id' is not provided.
        - 404 Not Found: If the student does not exist.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 15/04/2025
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        admissionNo = request.data.get('admissionNo')
        if not admissionNo:
            return Response({"error": "admissionNo is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = StudentData.objects.get(admissionNo=admissionNo)
            batch = student.batch
            student.delete()
            batch.reorderstudents()
            return Response({"message": "Student removed from batch"}, status=status.HTTP_200_OK)
        except StudentData.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)