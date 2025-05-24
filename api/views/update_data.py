from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import *
from api.serializers import *
from rest_framework import status
from api.permissions import isTeacher, isStudent
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.db.models import Q

class UpdateStudentData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher | isStudent]

    def post(self, request):
        data = request.data

        admission_no = None

        userProfile = UserProfile.objects.get(user_id=data.id)
        if userProfile.role == 'teacher':
            admission_no = data.get('admission_no')
            if not admission_no:
                return Response({"error": "admission_no is required as you are a teacher"}, status=status.HTTP_400_BAD_REQUEST)
        elif userProfile.role == 'student':
            admission_no = userProfile.dbUniqueID
        student = StudentData.objects.filter(admissionNo=admission_no).first()

        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentRegistrationSerializer(student, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateBatchData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        data = request.data
        batch_id = data.get('batch_id')
        if not batch_id:
            return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        batch = Batch.objects.filter(id=batch_id).first()

        if not batch:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BatchSerializer(batch, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateSessionData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        data = request.data
        session_id = data.get('session_id')
        if not session_id:
            return Response({"error": "session_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        session = Session.objects.filter(id=session_id).first()

        if not session:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SessionSerializer(session, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTeacherData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isTeacher]

    def post(self, request):
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        teacher = Teacher.objects.get(id=userProfile.dbUniqueID)

        if not teacher:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)