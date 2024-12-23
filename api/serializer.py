from rest_framework import serializers
from api.models import StudentData, Batch

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ["admissionNo", "studentPassword"]

class BatchCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["batchName", "description", "batchIncharge"]

class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = [
            "studentName", "studentClass", "division", 
            "gender", "fatherName", "email", "contactNo", "joinedDate", 
            "studentPassword", "batch", "profilePic"
        ]