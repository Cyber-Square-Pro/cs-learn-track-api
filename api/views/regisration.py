from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.helper import create_user
from api.permissions import isTeacher
from rest_framework_simplejwt.authentication import JWTAuthentication

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
            return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})
        
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        teacher = Teacher.objects.get(id=userProfile.dbUniqueID)

        serializer.save(batchIncharge=teacher)

        return Response({"message": "Batch created successfully", "status": status.HTTP_201_CREATED})

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
            return Response({"message": "Invalid data", "errors": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})
        
        student_data = serializer.validated_data

        # Check if the batch exists
        try:
            batch = Batch.objects.get(id=student_data["batch"].id)
        except Batch.DoesNotExist:
            return Response({"message": "Batch does not exist", "status": status.HTTP_400_BAD_REQUEST})

        # Generate admission number
        last_student = StudentData.objects.order_by('admissionNo').last()
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
            profilePic=student_data.get("profilePic")
        )

        # Create user account
        create_user(
            username=student.admissionNo,
            password=student.studentPassword,
            email=student.email,
            role="student"
        )
        # Update roll numbers in the batch
        students_in_batch = StudentData.objects.filter(batch=batch).order_by('studentName')
        for index, student in enumerate(students_in_batch, start=1):
            student.rollNo = index
            student.save()

        return Response({"message": "Student registered successfully", "admissionNo": admission_no, "status": status.HTTP_201_CREATED})

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
            return Response({"message": "Invalid data", "errors": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})
        
        teacher_data = serializer.validated_data

        # Save teacher data
        teacher = Teacher.objects.create(
            name=teacher_data["name"],
            email=teacher_data["email"],
            contactNo=teacher_data["contactNo"],
            hireDate=teacher_data["hireDate"],
            teacherPassword=teacher_data["teacherPassword"],
            profilePic=teacher_data.get("profilePic")
        )

        # Create user account
        create_user(
            username=teacher.id,
            password=teacher.teacherPassword,
            email=teacher.email,
            role="teacher"
        )

        return Response({"message": "Teacher registered successfully", "status": status.HTTP_201_CREATED})
