from rest_framework import serializers
from db.models import Batch, Session, Teacher

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


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name', 'subject', 'contactNo', 'profilePic']
        read_only_fields = ['id', 'email', 'hireDate']