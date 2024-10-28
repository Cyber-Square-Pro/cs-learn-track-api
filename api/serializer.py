from rest_framework import serializers
from .models import AdminAccess

class AdminAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccess
        fields = ['username', 'password']