from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.permissions import isTeacher, isStudent
from rest_framework_simplejwt.authentication import JWTAuthentication

class CheckUserTypeEndPoint(APIView):
    """
    CheckUserTypeEndPoint is an API endpoint that verifies the type of user 
    (either teacher or student) based on the provided JWT token.
    Attributes:
        authentication_classes (list): List of authentication classes to use for this view.
        permission_classes (list): List of permission classes to use for this view.
    Methods:
        post(request):
            Handles POST requests to check the user type.
            Returns a JSON response with the user's role if the token is valid,
            otherwise returns an error message.
    
    Responses: 
        - 200 OK: If the request is successful.
        - 400 Bad Request: If the JWT token is invalid.

    Created by: Yash Raj on 11/01/2024
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher, isStudent]

    def post(self, request):
        if not request.user.id:
            return Response({"message": "Invalid User Token", "status": status.HTTP_400_BAD_REQUEST})
        
        userProfile = UserProfile.objects.get(user_id=request.user.id)

        return Response({"role": userProfile.role, "status": status.HTTP_200_OK})

class ListBatchEndPoint(APIView):
    """
    API endpoint to list all batches a teacher is in charge of.

    This endpoint handles GET requests and returns a dictionary of batches.

    Methods:
        get(request): 
            Returns a dictionary of batches the teacher is in charge of.

    Responses:
        - 200 OK: If the request is successful.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 11/01/2024
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        teacher = Teacher.objects.get(id=userProfile.dbUniqueID)
        batches = Batch.objects.filter(batchIncharge=teacher)
        
        batch_list = [{"id": batch.id, "name": batch.batchName} for batch in batches]
        
        return Response({"batches": batch_list, "status": status.HTTP_200_OK})

class GetTeacherData(APIView):
    """
    API endpoint to get all data of a teacher.

    This endpoint handles GET requests and returns all the data of the teacher.

    Methods:
        get(request): 
            Returns all data of the teacher.

    Responses:
        - 200 OK: If the request is successful.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 11/01/2024
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        teacher = Teacher.objects.get(id=userProfile.dbUniqueID)
        teacher_data = {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "contactNo": teacher.contactNo,
            "hireDate": teacher.hireDate,
            "teacherPassword": teacher.teacherPassword,
            "profilePic": teacher.profilePic.url if teacher.profilePic else None
        }
        return Response({"teacher_data": teacher_data, "status": status.HTTP_200_OK})

class GetStudentData(APIView):
    """
    API endpoint to get all data of a student.

    This endpoint handles GET requests and returns all the data of the student.

    Methods:
        get(request): 
            Returns all data of the student.

    Responses:
        - 200 OK: If the request is successful.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 11/01/2024
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isStudent]

    def post(self, request):
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        student = StudentData.objects.get(admissionNo=userProfile.dbUniqueID)
        student_data = {
            "admissionNo": student.admissionNo,
            "studentName": student.studentName,
            "rollNo": student.rollNo,
            "studentClass": student.studentClass,
            "division": student.division,
            "gender": student.gender,
            "fatherName": student.fatherName,
            "email": student.email,
            "contactNo": student.contactNo,
            "joinedDate": student.joinedDate,
            "studentPassword": student.studentPassword,
            "profilePic": student.profilePic.url if student.profilePic else None
        }
        return Response({"student_data": student_data, "status": status.HTTP_200_OK})

