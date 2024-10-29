from rest_framework import serializers
from api.models import Studentdata

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studentdata
        fields = ["studentID", "studentPassword"]