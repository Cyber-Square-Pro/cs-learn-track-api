from rest_framework import serializers
from .models import AdminData

class AdminDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminData
        fields = ['username', 'password']