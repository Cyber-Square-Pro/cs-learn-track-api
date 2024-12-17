from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from api.models import StudentData, Batch
from api.serializer import StudentLoginSerializer, BatchCreationSerializer, StudentRegistrationSerializer
from rest_framework import status

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
        serializer = StudentLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})
        student_data = serializer.validated_data

        if not StudentData.objects.filter(admissionNo=student_data["admissionNo"]).exists():
            return Response({"message": "Student does not exist", "status": status.HTTP_400_BAD_REQUEST})
        
        if StudentData.objects.get(admissionNo=student_data["admissionNo"]).studentPassword == student_data["studentPassword"]:
            return Response({"message": "Student logged in successfully", "status": status.HTTP_200_OK})
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
            accountStatus=student_data["accountStatus"],
            studentPassword=student_data["studentPassword"],
            batch=batch,
            profilePic=student_data.get("profilePic")
        )

        # Update roll numbers in the batch
        students_in_batch = StudentData.objects.filter(batch=batch).order_by('studentName')
        for index, student in enumerate(students_in_batch, start=1):
            student.rollNo = index
            student.save()

        return Response({"message": "Student registered successfully", "status": status.HTTP_201_CREATED})