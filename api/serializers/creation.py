from rest_framework import serializers
from db.models import Batch

class BatchCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["batchName", "description"]