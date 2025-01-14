from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


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
    
    Created by: Yash Raj on 11/01/2024
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
            return Response({"message": "Invalid password", "status": status.HTTP_400_BAD_REQUEST})

class StudentLoginEndPoint(APIView):
    """
    API endpoint for student login.

    This endpoint handles POST requests for student login. It validates the provided
    student credentials and checks if the student exists in the database. 

    Methods:
        post(request): 
            Handles the login process for students. It expects a JSON payload with 
            'admissionNo' and 'studentPassword'. If the credentials are valid, it returns 
            a success message; otherwise, it returns an appropriate error message.

    Responses:
        - 200 OK: If the student is successfully logged in.
        - 400 Bad Request: If the provided data is invalid, the student does not exist, 
          or the password is incorrect.
    
    Created by: Yash Raj on 11/01/2024
    """
    def post(self, request):
        admission_no = request.data.get("admissionNo")
        student_password = request.data.get("studentPassword")

        if not admission_no or not student_password:
            return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})

        if not StudentData.objects.filter(admissionNo=admission_no).exists():
            return Response({"message": "Student does not exist", "status": status.HTTP_400_BAD_REQUEST})
        
        student = StudentData.objects.get(admissionNo=admission_no)
        if student.studentPassword == student_password:
            userProfile = UserProfile.objects.filter(role="student").get(dbUniqueID=student.admissionNo)
            user = User.objects.get(id=userProfile.user_id)
            userProfile.active = True
            userProfile.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Student logged in successfully",
                "status": status.HTTP_200_OK,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        else:
            return Response({"message": "Invalid password", "status": status.HTTP_400_BAD_REQUEST})

class TeacherLoginEndPoint(APIView):
    """
    API endpoint for teacher login.

    This endpoint handles POST requests for teacher login. It validates the provided
    teacher credentials and checks if the teacher exists in the database. 

    Methods:
        post(request): 
            Handles the login process for teachers. It expects a JSON payload with 
            'email' and 'teacherPassword'. If the credentials are valid, it returns 
            a success message; otherwise, it returns an appropriate error message.

    Responses:
        - 200 OK: If the teacher is successfully logged in.
        - 400 Bad Request: If the provided data is invalid, the teacher does not exist, 
            or the password is incorrect.

    Created by: Yash Raj on 11/01/2024
    """
    def post(self, request):
        email = request.data.get("email")
        teacher_password = request.data.get("teacherPassword")

        if not email or not teacher_password:
            return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})

        if not Teacher.objects.filter(email=email).exists():
            return Response({"message": "Teacher does not exist", "status": status.HTTP_400_BAD_REQUEST})
        
        teacher = Teacher.objects.get(email=email)


        if teacher.teacherPassword == teacher_password:
            userProfile = UserProfile.objects.filter(role="teacher").get(dbUniqueID=teacher.id)
            user = User.objects.get(id=userProfile.user_id)
            userProfile.active = True
            userProfile.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Teacher logged in successfully",
                "teacher_name": teacher.name,
                "status": status.HTTP_200_OK,
                "access": str(refresh.access_token)
            })
        else:
            return Response({"message": "Invalid password", "status": status.HTTP_400_BAD_REQUEST})

class LogoutEndPoint(APIView):
    """
    API endpoint for user logout.

    This endpoint handles POST requests for user logout. It invalidates the user's token
    and logs them out.

    Methods:
        post(request): 
            Handles the logout process for users. It invalidates the user's token and logs them out.

    Responses:
        - 200 OK: If the user is successfully logged out.
        - 400 Bad Request: If the token is invalid or not provided.

    Created by: Yash Raj on 14/01/2024
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        userProfile.active = False
        userProfile.save()

        return Response({"message": "Logged out successfully", "status": status.HTTP_200_OK})