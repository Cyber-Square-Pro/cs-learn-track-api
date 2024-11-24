from rest_framework import serializers
from api.models import StudentData, Batch

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ["studentID", "studentPassword"]

class BatchCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["name", "description", "grade", "section"]