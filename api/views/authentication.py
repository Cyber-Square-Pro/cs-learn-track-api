from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import isStudent
from db.models import *
from api.serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import face_recognition
import numpy as np
from PIL import Image
import io
import base64

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
    
    Created by: Yash Raj on 11/01/2025
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
    
    Created by: Yash Raj on 11/01/2025
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
                "name": student.studentName,
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

    Created by: Yash Raj on 11/01/2025
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
                "name": teacher.name,
                "status": status.HTTP_200_OK,
                "refresh": str(refresh),
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

    Created by: Yash Raj on 14/01/2025
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response({"message": "Invalid token", "status": status.HTTP_400_BAD_REQUEST, "error": str(e)})

        userProfile = UserProfile.objects.get(user_id=request.user.id)
        userProfile.active = False
        userProfile.save()

        return Response({"message": "Logged out successfully", "status": status.HTTP_200_OK})

class RegenerateAccessToken(APIView):
    """
    API endpoint to regenerate access token.

    This endpoint handles POST requests to regenerate an access token using a refresh token.
    It validates the provided refresh token and returns a new access token if valid.

    Methods:
        post(request): 
            Handles the token regeneration process. It expects a JSON payload with 
            'refresh'. If the token is valid, it returns a new access token; otherwise, 
            it returns an appropriate error message.

    Responses:
        - 200 OK: If the token is successfully regenerated.
        - 400 Bad Request: If the provided token is invalid.

    Created by: Yash Raj on 22/01/2025
    """
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.check_blacklist()
                return Response({
                    "access": str(token.access_token),
                    "status": status.HTTP_200_OK
                })
            except Exception as e:
                return Response({"message": "Invalid token", "status": status.HTTP_400_BAD_REQUEST})
        return Response({"message": "Invalid token", "status": status.HTTP_400_BAD_REQUEST})


class AddFaceEncodingEndPoint(APIView):
    """
    API endpoint to add face encoding.

    This endpoint handles POST requests to add face encoding for a user. It expects
    a JSON payload with 'face_image'. If the data is valid, it saves
    the face encoding to the database.

    Methods:
        post(request): 
            Handles the addition of face encoding. It expects a JSON payload with 
            'face_image'. If successful, it returns a success message; 
            otherwise, it returns an appropriate error message.

    Responses:
        - 200 OK: If the face encoding is successfully added.
        - 400 Bad Request: If the provided data is invalid or if the user does not exist.

    Created by: Yash Raj on 24/05/2025
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [isStudent]

    def post(self, request):
        user_profile = UserProfile.objects.get(user_id=request.user.id)
        if user_profile.role != "student":
            return Response({"message": "Only students can add face encoding", "status": status.HTTP_403_FORBIDDEN})
        student = StudentData.objects.get(admissionNo=user_profile.dbUniqueID)

        face_recognition_image = request.data.get("face_image")
        if not face_recognition_image:
            return Response({"message": "Face image is required", "status": status.HTTP_400_BAD_REQUEST})
        
        try:
            # For base64 string handling
            # If the string contains a prefix like "data:image/jpeg;base64,"
            if ';base64,' in face_recognition_image:
                format, imgstr = face_recognition_image.split(';base64,')
                image_data = base64.b64decode(imgstr)
            else:
                # If it's just the base64 string without the prefix
                image_data = base64.b64decode(face_recognition_image)
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to numpy array for face_recognition
            image_array = np.array(image)
            
            # Detect faces in the image
            face_locations = face_recognition.face_locations(image_array)
            if not face_locations:
                return Response({"message": "No face detected in the image", "status": status.HTTP_400_BAD_REQUEST})
            
            # Get the encoding for the first face found
            face_encoding = face_recognition.face_encodings(image_array, face_locations)[0]
            
            # Convert numpy array to binary for database storage
            face_encoding_binary = face_encoding.tobytes()
            
            # Save the encoding to the student record
            student.faceEncoding = face_encoding_binary
            student.profilePic = face_recognition_image  # Saving the image data as profile picture (it is always image/jpeg as a base64 string)
            student.save()
            
            return Response({"message": "Face encoding added successfully", "status": status.HTTP_200_OK})
            
        except Exception as e:
            return Response({
                "message": "Error processing face image", 
                "error": str(e),
                "status": status.HTTP_400_BAD_REQUEST
            })

class LoginFaceEndPoint(APIView):
    def post(self, request):
        admission_no = request.data.get("admissionNo")
        if not admission_no:
            return Response({"message": "Admission number is required", "status": status.HTTP_400_BAD_REQUEST})
        
        student = StudentData.objects.filter(admissionNo=admission_no).first()
        if not student:
            return Response({"message": "Student does not exist", "status": status.HTTP_400_BAD_REQUEST})

        auth_encoding_binary = student.faceEncoding
        if not auth_encoding_binary:
            return Response({"message": "Face encoding not found for the student", "status": status.HTTP_400_BAD_REQUEST})

        login_image = request.data.get("login_image")
        if not login_image:
            return Response({"message": "Face image is required", "status": status.HTTP_400_BAD_REQUEST})
        
        try:
            # For base64 string handling
            # If the string contains a prefix like "data:image/jpeg;base64,"
            if ';base64,' in login_image:
                format, imgstr = login_image.split(';base64,')
                image_data = base64.b64decode(imgstr)
            else:
                # If it's just the base64 string without the prefix
                image_data = base64.b64decode(login_image)

             # Convert to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to numpy array for face_recognition
            image_array = np.array(image)
            
            # Detect faces in the image
            face_locations = face_recognition.face_locations(image_array)
            if not face_locations:
                return Response({"message": "No face detected in the image", "status": status.HTTP_400_BAD_REQUEST})
            
            # Get the encoding for the first face found
            face_encoding = face_recognition.face_encodings(image_array, face_locations)[0]
            auth_encoding = np.frombuffer(auth_encoding_binary, dtype=np.float64)

            results = face_recognition.compare_faces([face_encoding], auth_encoding)

            if results[0]:
                userProfile = UserProfile.objects.filter(role="student").get(dbUniqueID=student.admissionNo)
                user = User.objects.get(id=userProfile.user_id)
                userProfile.active = True
                userProfile.save()

                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Student logged in successfully",
                    "name": student.studentName,
                    "status": status.HTTP_200_OK,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
            else:
                return Response({"message": "Face does not match", "status": status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            return Response({
                "message": "Error processing face image", 
                "error": str(e),
                "status": status.HTTP_400_BAD_REQUEST
            })
            