from rest_framework import serializers
from .models import AdminAccess, Student, Attendance

class AdminAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccess
        fields = ['username', 'password']