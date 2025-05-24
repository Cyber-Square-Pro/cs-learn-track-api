from rest_framework import serializers
from db.models.batch import Batch, Session

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


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'sessionName', 'batch', 'createdBy', 'startDateTime', 'endDateTime']
        read_only_fields = ['id', 'createdBy']