from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.permissions import isTeacher, isStudent
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime, timedelta

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

    Created by: Yash Raj on 11/01/2025
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

    This endpoint handles POST requests and returns a dictionary of batches.

    Methods:
        post(request): 
            Returns a dictionary of batches the teacher is in charge of.

    Responses:
        - 200 OK: If the request is successful.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 11/01/2025
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        teacher = Teacher.objects.get(id=userProfile.dbUniqueID)
        batches_incharge = Batch.objects.filter(batchIncharge=teacher)
        batches_teaching = Batch.objects.filter(teachers=teacher)
        batches = batches_incharge.union(batches_teaching)
        
        batch_list = [{"id": batch.id, "name": batch.batchName} for batch in batches]
        
        return Response({"batches": batch_list, "status": status.HTTP_200_OK})

class GetTeacherData(APIView):
    """
    API endpoint to get all data of a teacher.

    This endpoint handles POST requests and returns all the data of the teacher.

    Methods:
        post(request): 
            Returns all data of the teacher.

    Responses:
        - 200 OK: If the request is successful.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 11/01/2025
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

    This endpoint handles POST requests and returns all the data of the student.

    Methods:
        post(request): 
            Returns all data of the student.

    Responses:
        - 200 OK: If the request is successful.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 11/01/2025
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
            "gender": student.gender,
            "fatherName": student.fatherName,
            "email": student.email,
            "contactNo": student.contactNo,
            "joinedDate": student.joinedDate,
            "studentPassword": student.studentPassword,
            "profilePic": student.profilePic.url if student.profilePic else None
        }
        return Response({"student_data": student_data, "status": status.HTTP_200_OK})

class GetTeacherDashboardDetails(APIView):
    """
    API endpoint to get the dashboard details of a teacher.

    This endpoint handles POST requests and returns the dashboard details of the teacher.

    Methods:
        post(request): 
            Returns the dashboard details of the teacher.

    Responses:
        - 200 OK: If the request is successful with the total number of students, active teachers, and last 3 active students.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 13/01/2025
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        total_students = StudentData.objects.count()
        active_students = UserProfile.objects.filter(role='student', active=True).count()

        recent_students_details = []
        recent_students = UserProfile.objects.filter(role='student').order_by('-last_login')[:3]
        for student in recent_students:
            student_data = StudentData.objects.get(admissionNo=student.dbUniqueID)
            student_data = {
                "admissionNo": student_data.admissionNo,
                "studentName": student_data.studentName,
                "batch": student_data.batch.batchName,
                "email": student_data.email,
                "active": student.active
            }
            recent_students_details.append(student_data)

        # Get teacher data
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        teacher = Teacher.objects.get(id=userProfile.dbUniqueID)

        # Get batches where this teacher is in charge or teaches
        # batches_incharge = Batch.objects.filter(batchIncharge=teacher)
        # batches_teaching = Batch.objects.filter(teachers=teacher)
        # batches = batches_incharge.union(batches_teaching)

        # Get batches where this teacher is in charge
        batches = Batch.objects.filter(batchIncharge=teacher)

        # Get attendance data for the last 4 days

        # Get the current date
        current_date = datetime.now().date()

        # Initialize data structure to store attendance percentage for last 4 days
        attendance_data = []

        # Calculate attendance for each of the last 4 days
        for i in range(4):
            day_date = current_date - timedelta(days=i)
            
            # Get sessions for this day that are for batches where this teacher is involved
            sessions = Session.objects.filter(batch__in=batches, startDateTime__date=day_date)
            
            # Initialize counters
            total_attendance_records = 0
            present_count = 0
            
            # Go through each session and count attendance
            for session in sessions:
                attendance_records = Attendance.objects.filter(session=session)
                total_attendance_records += attendance_records.count()
                present_count += attendance_records.filter(status=True).count()
            
            # Calculate percentage (avoid division by zero)
            attendance_percentage = 0
            if total_attendance_records > 0:
                attendance_percentage = (present_count / total_attendance_records) * 100
            
            # Add to our data
            attendance_data.append({
                "date": day_date.strftime('%d-%m-%Y'),
                "percentage": round(attendance_percentage, 2)
            })

        return Response({"total_students": total_students, "active_students": active_students, "recent_students_details": recent_students_details, "attendance_data": attendance_data, "status": status.HTTP_200_OK})

class TeacherGetStudentData(APIView):
    """
    API endpoint for teachers to retrieve all data of a specific student by admission number.

    This endpoint handles POST requests and returns all the data of the student whose admission number is provided in the request body.

    Methods:
        post(request): 
            Accepts an "admissionNo" in the request data and returns all data of the corresponding student.

    Responses:
        - 200 OK: If the student is found and data is returned successfully.
        - 400 Bad Request: If the admission number is not provided.
        - 404 Not Found: If no student exists with the given admission number.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 18/01/2025
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        admission_num = request.data.get("admissionNo")
        if not admission_num:
            return Response({"message": "Admission number is required", "status": status.HTTP_400_BAD_REQUEST})
        try:
            student = StudentData.objects.get(admissionNo=admission_num)
        except StudentData.DoesNotExist:
            return Response({"message": "Student not found", "status": status.HTTP_404_NOT_FOUND})
        
        student_data = {
            "admissionNo": student.admissionNo,
            "studentName": student.studentName,
            "rollNo": student.rollNo,
            "studentClass": student.studentClass,
            "gender": student.gender,
            "fatherName": student.fatherName,
            "email": student.email,
            "contactNo": student.contactNo,
            "joinedDate": student.joinedDate,
            "studentPassword": student.studentPassword,
            "profilePic": student.profilePic.url if student.profilePic else None
        }
        return Response({"student_data": student_data, "status": status.HTTP_200_OK})

class GetSessionAttendace(APIView):
    """
    API endpoint to get the attendance of a specific session.

    This endpoint handles POST requests and returns the attendance details of the session specified by its ID.

    Methods:
        post(request): 
            Accepts a "sessionId" in the request data and returns the attendance details for that session.

    Responses:
        - 200 OK: If the session is found and attendance data is returned successfully.
        - 400 Bad Request: If the session ID is not provided.
        - 404 Not Found: If no session exists with the given ID.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 24/05/2025
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        session_id = request.data.get("session_id")
        if not session_id:
            return Response({"message": "Session ID is required", "status": status.HTTP_400_BAD_REQUEST})
        
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({"message": "Session not found", "status": status.HTTP_404_NOT_FOUND})
        
        attendance_records = Attendance.objects.filter(session=session)
        attendance_data = []
        
        for record in attendance_records:
            student_data = {
                "admissionNo": record.student.admissionNo,
                "studentName": record.student.studentName,
                "status": record.status
            }
            attendance_data.append(student_data)
        
        return Response({"attendance_data": attendance_data, "status": status.HTTP_200_OK}) 
