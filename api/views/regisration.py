from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.helper import create_user
from api.permissions import isTeacher
from rest_framework_simplejwt.authentication import JWTAuthentication
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

class BatchCreationEndPoint(APIView):
    """
    API endpoint for batch creation.

    This endpoint handles POST requests for creating a new batch. It validates the provided
    batch data and saves it to the database.

    Methods:
        post(request):
            Handles the batch creation process. It expects a JSON payload with batch details.
            If the data is valid, it creates a new batch and returns a success message.

    Responses:
        - 201 Created: If the batch is successfully created.
        - 400 Bad Request: If the provided data is invalid.

    Created by: Yash Raj on 11/01/2025
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        serializer = BatchCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": "Invalid data",
                    "errors": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )

        userProfile = UserProfile.objects.get(user_id=request.user.id)
        teacher = Teacher.objects.get(id=userProfile.dbUniqueID)

        serializer.save(batchIncharge=teacher)

        return Response(
            {"message": "Batch created successfully", "status": status.HTTP_201_CREATED}
        )


class RegisterStudentEndPoint(APIView):
    """
    API endpoint for student registration.

    This endpoint handles POST requests for registering a new student. It validates the provided
    student data and saves it to the database. The admission number is auto-generated based on the
    last student's admission number in the database.

    Methods:
        post(request):
            Handles the student registration process. It expects a JSON payload with student details.
            If the data is valid, it registers the student and returns a success message.

    Responses:
        - 201 Created: If the student is successfully registered.
        - 400 Bad Request: If the provided data is invalid or the batch does not exist.
        - 500 Internal Server Error: If there is an error during the registration process.

    Created by: Yash Raj on 11/01/2025
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": "Invalid data",
                    "errors": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )

        student_data = serializer.validated_data

        # Check if the batch exists
        try:
            batch = Batch.objects.get(id=student_data["batch"].id)
        except Batch.DoesNotExist:
            return Response(
                {
                    "message": "Batch does not exist",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )

        # Generate admission number
        last_student = StudentData.objects.order_by("admissionNo").last()
        if last_student:
            admission_no = last_student.admissionNo + 1
        else:
            admission_no = 1000  # Starting admission number

        # Save student data
        student = StudentData.objects.create(
            studentName=student_data["studentName"],
            admissionNo=admission_no,
            rollNo=0,  # Placeholder, will be updated later
            studentClass=student_data["studentClass"],
            division=student_data["division"],
            gender=student_data["gender"],
            fatherName=student_data["fatherName"],
            email=student_data["email"],
            contactNo=student_data["contactNo"],
            joinedDate=student_data["joinedDate"],
            # accountStatus=student_data["accountStatus"],
            studentPassword=student_data["studentPassword"],
            batch=batch,
            profilePic=None,
        )

        # Create user account
        create_user(
            username=student.admissionNo,
            password=student.studentPassword,
            email=student.email,
            role="student",
        )
        
        batch.reorderstudents()

        return Response(
            {
                "message": "Student registered successfully",
                "admissionNo": admission_no,
                "status": status.HTTP_201_CREATED,
            }
        )


class RegisterTeacherEndPoint(APIView):
    """
    API endpoint for teacher registration.

    This endpoint handles POST requests for registering a new teacher. It validates the provided
    teacher data and saves it to the database.

    Methods:
        post(request):
            Handles the teacher registration process. It expects a JSON payload with teacher details.
            If the data is valid, it registers the teacher and returns a success message.

    Responses:
        - 201 Created: If the teacher is successfully registered.
        - 400 Bad Request: If the provided data is invalid.
        - 500 Internal Server Error: If there is an error during the registration process.

    Created by: Yash Raj on 11/01/2025
    """

    def post(self, request):
        serializer = TeacherRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": "Invalid data",
                    "errors": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )

        teacher_data = serializer.validated_data

        # Save teacher data
        teacher = Teacher.objects.create(
            name=teacher_data["name"],
            email=teacher_data["email"],
            contactNo=teacher_data["contactNo"],
            hireDate=teacher_data["hireDate"],
            teacherPassword=teacher_data["teacherPassword"],
            profilePic=teacher_data.get("profilePic"),
        )

        # Create user account
        create_user(
            username=teacher.id,
            password=teacher.teacherPassword,
            email=teacher.email,
            role="teacher",
        )

        return Response(
            {
                "message": "Teacher registered successfully",
                "status": status.HTTP_201_CREATED,
            }
        )


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