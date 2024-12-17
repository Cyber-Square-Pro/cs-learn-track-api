from rest_framework import serializers
from api.models import StudentData, Batch

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ["admissionNo", "studentPassword"]

class BatchCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["description", "grade", "section", "seatNumber"]

class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = [
            "studentName", "admissionNo", "rollNo", "studentClass", "division", 
            "gender", "fatherName", "email", "contactNo", "joinedDate", 
            "accountStatus", "studentPassword", "batch", "profilePic"
        ]