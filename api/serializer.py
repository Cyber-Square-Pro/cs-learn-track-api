from rest_framework import serializers
from api.models import StudentData

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ["studentID", "studentPassword"]