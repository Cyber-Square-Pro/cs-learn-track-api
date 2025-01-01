from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from api.models import StudentData, Batch, Teacher
from api.serializer import StudentLoginSerializer, BatchCreationSerializer, StudentRegistrationSerializer, TeacherRegistrationSerializer
from rest_framework import status
from api.helper_funcs import create_user
from rest_framework_simplejwt.tokens import RefreshToken
from api.permissions import isTeacher, isStudent
from rest_framework_simplejwt.authentication import JWTAuthentication


class LandingEndPoint(APIView):
    """
    API endpoint for landing page.

    This endpoint handles GET requests and returns a welcome message.

    Methods:
        get(request): 
            Returns a welcome message in HTML format.

    Responses:
        - 200 OK: Always returns a welcome message.
    """
    def get(self, request):
        return HttpResponse('<h1 align="center" style="margin-top:200px">Welcome Onboard!..</h1>')

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
            refresh = RefreshToken.for_user(student)
            return Response({
                "message": "Student logged in successfully",
                "status": status.HTTP_200_OK,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        else:
            return Response({"message": "Invalid password", "status": status.HTTP_400_BAD_REQUEST})

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
    """
    def post(self, request):
        serializer = BatchCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})
        
        serializer.save()
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
    """
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

        return Response({"message": "Student registered successfully", "status": status.HTTP_201_CREATED})

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

class AuthTest(APIView):
    """
    API endpoint to test JWT authentication for students.

    This endpoint handles GET requests and checks if the provided JWT token is valid.

    Methods:
        get(request): 
            Returns a success message if the JWT token is valid.

    Responses:
        - 200 OK: If the JWT token is valid.
        - 401 Unauthorized: If the JWT token is invalid or not provided.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isStudent]

    def get(self, request):
        return Response({"message": "JWT token is valid", "status": status.HTTP_200_OK})