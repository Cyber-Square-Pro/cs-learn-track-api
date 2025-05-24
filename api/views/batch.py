from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.permissions import isTeacher, isStudent
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.db.models import Q


class GetBatchStudentList(APIView):
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
        batch_id = request.data.get("batch_id")
        if not batch_id:
            return Response(
                {"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            batch = Batch.objects.get(id=batch_id)
            students = StudentData.objects.filter(batch=batch).order_by("rollNo")
            data = {
                "batch": batch.batchName,
                "students": [
                    {
                        "name": student.studentName,
                        "email": student.email,
                        "admissionNo": student.admissionNo,
                    }
                    for student in students
                ],
            }
            return Response(data, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return Response(
                {"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND
            )


class GetTeacherStudentList(APIView):
    """
    API endpoint to retrieve the list of students for a teacher.

    This endpoint handles POST requests and returns the list of students in batches where the teacher is the incharge.

    Methods:
        post(request):
            Returns the list of students in batches where the teacher is the incharge.

    Responses:
        - 200 OK: If the teacher is found and students are returned.
        - 404 Not Found: If the teacher does not exist or has no students.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Updated by: Yash Raj on 18/04/2025
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        try:
            userProfile = UserProfile.objects.get(user_id=request.user.id)
            teacher = Teacher.objects.get(id=userProfile.dbUniqueID)
            batches = Batch.objects.filter(batchIncharge=teacher)
            student_list = StudentData.objects.filter(batch__in=batches).order_by(
                "rollNo"
            )
            data = {
                "students": [
                    {
                        "name": student.studentName,
                        "rollNo": student.rollNo,
                        "admissionNo": student.admissionNo,
                        "batch": student.batch.batchName,
                    }
                    for student in student_list
                ]
            }
            return Response(data, status=status.HTTP_200_OK)
        except (UserProfile.DoesNotExist, Teacher.DoesNotExist):
            return Response(
                {"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND
            )


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
        admissionNo = request.data.get("admissionNo")
        if not admissionNo:
            return Response(
                {"error": "admissionNo is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            student = StudentData.objects.get(admissionNo=admissionNo)
            userprofile = UserProfile.objects.get(dbUniqueID=student.admissionNo)
            auth_user = User.objects.get(id=userprofile.user_id)
            batch = student.batch
            student.delete()
            userprofile.delete()
            auth_user.delete()

            batch.reorderstudents()
            return Response(
                {"message": "Student removed from batch"}, status=status.HTTP_200_OK
            )
        except StudentData.DoesNotExist:
            return Response(
                {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CreateSession(APIView):
    """
    API endpoint to create a session for a batch.

    This endpoint handles POST requests and creates a session with the specified details.

    Methods:
        post(request):
            Expects 'sessionName', 'batch_id', 'startDateTime', and 'endDateTime' in the request data.

    Responses:
        - 201 Created: If the session is successfully created.
        - 400 Bad Request: If any required field is missing or invalid.
        - 409 Conflict: If the session conflicts with an existing session.
        - 404 Not Found: If the batch does not exist.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 24/05/2025
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        session_name = request.data.get("sessionName")
        batch_id = request.data.get("batch_id")
        start_date_time = request.data.get("startDateTime")
        end_date_time = request.data.get("endDateTime")
        
        # Validate required fields
        if not all([session_name, batch_id, start_date_time, end_date_time]):
            return Response(
                {"error": "sessionName, batch_id, startDateTime, and endDateTime are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            batch = Batch.objects.get(id=batch_id)
            
            # Check for schedule conflicts
            conflicts = Session.objects.filter(
                batch=batch,
                # Find overlapping sessions:
                # - New session starts during an existing session
                # - New session ends during an existing session
                # - New session completely encloses an existing session
                # - New session is completely enclosed by an existing session
            ).filter(
                    # This checks for overlapping sessions but excludes exactly adjacent sessions
                    (Q(startDateTime__lt=end_date_time) & Q(endDateTime__gt=start_date_time)) & 
                    ~(Q(startDateTime=end_date_time) | Q(endDateTime=start_date_time))
            )
            
            if conflicts.exists():
                conflicting_sessions = [
                    {
                        "id": session.id,
                        "sessionName": session.sessionName,
                        "startDateTime": session.startDateTime,
                        "endDateTime": session.endDateTime,
                    }
                    for session in conflicts
                ]
                return Response(
                    {
                        "error": "Session time conflicts with existing sessions",
                        "conflicts": conflicting_sessions
                    }, 
                    status=status.HTTP_409_CONFLICT
                )
            
            userProfile = UserProfile.objects.get(user_id=request.user.id)
            teacher = Teacher.objects.get(id=userProfile.dbUniqueID)

            # Create session directly
            session = Session.objects.create(
                sessionName=session_name,
                batch=batch,
                startDateTime=start_date_time,
                endDateTime=end_date_time,
                createdBy=teacher
            )
            
            # Return the created session data
            data = {
                "id": session.id,
                "sessionName": session.sessionName,
                "batch_id": session.batch.id,
                "startDateTime": session.startDateTime,
                "endDateTime": session.endDateTime,
            }
            
            return Response(data, status=status.HTTP_201_CREATED)
            
        except Batch.DoesNotExist:
            return Response(
                {"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class GetBatchSessions(APIView):
    """
    API endpoint to retrieve all sessions for a given batch.

    This endpoint handles POST requests and returns the list of sessions for the specified batch.

    Methods:
        post(request):
            Expects 'batch_id' in the request data and returns the list of sessions.

    Responses:
        - 200 OK: If the batch is found and sessions are returned.
        - 400 Bad Request: If 'batch_id' is not provided.
        - 404 Not Found: If the batch does not exist.
        - 401 Unauthorized: If the JWT token is invalid or not provided.

    Created by: Yash Raj on 24/05/2025
    """

    authentication_classes = [JWTAuthentication]

    def post(self, request):
        batch_id = request.data.get("batch_id")
        if not batch_id:
            return Response(
                {"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            batch = Batch.objects.get(id=batch_id)
            sessions = Session.objects.filter(batch=batch).order_by("startDateTime")
            data = {
                "batch_name": batch.batchName,
                "batch_id": batch.id,
                "sessions": [
                    {
                        "id": session.id,
                        "sessionName": session.sessionName,
                        "startDateTime": session.startDateTime,
                        "endDateTime": session.endDateTime,
                        "createdBy": session.createdBy.name if session.createdBy else None,
                    }
                    for session in sessions
                ],
            }
            return Response(data, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return Response(
                {"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND
            )


class MarkAttendanceEndPoint(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        session_id = request.data.get("session_id")
        if not session_id:
            return Response({"error": "Session ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        session = Session.objects.filter(id=session_id).first()
        if not session:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        attendance_data = request.data.get("attendance", [])  # List of admission numbers of present students
        if not attendance_data:
            return Response({"error": "Attendance data is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Get batch from the session
        batch = session.batch
        if not batch:
            return Response({"error": "No batch associated with this session"}, status=status.HTTP_404_NOT_FOUND)
            
        # Get all students in the batch
        students = StudentData.objects.filter(batch=batch)
            
        # Mark attendance for each student
        for student in students:
            # Check if student's admission number is in the list of present students
            is_present = student.admissionNo in attendance_data
            
            # Update or create attendance record
            Attendance.objects.update_or_create(
                session=session,
                student=student,
                defaults={"status": is_present}
            )
        return Response({"message": "Attendance marked successfully"}, status=status.HTTP_200_OK)