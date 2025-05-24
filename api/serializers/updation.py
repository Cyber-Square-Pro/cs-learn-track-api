from rest_framework import serializers
from db.models.batch import Batch

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = [
            'id',
            'batchName',
            'description',
            'batchStatus',
            'createdAt',
            'batchIncharge',
            'teachers',
        ]
        read_only_fields = ['id', 'createdAt']