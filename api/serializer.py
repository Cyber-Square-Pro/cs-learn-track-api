from rest_framework import serializers
from api.models import StudentData, Batch, AdminData, Teacher

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ["admissionNo", "studentPassword"]

class BatchCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["batchName", "description"]

class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = [
            "studentName", "studentClass", "division", 
            "gender", "fatherName", "email", "contactNo", "joinedDate", 
            "studentPassword", "batch", "profilePic"
        ]

class AdminDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminData
        fields = ['username', 'password']


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "name", "email", "contactNo", "hireDate", 
            "teacherPassword", "profilePic"
        ]
