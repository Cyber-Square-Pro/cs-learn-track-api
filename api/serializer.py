from rest_framework import serializers
from api.models import StudentData
from api.models import AdminData

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ["studentID", "studentPassword"]

class AdminDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminData
        fields = ['username', 'password']
