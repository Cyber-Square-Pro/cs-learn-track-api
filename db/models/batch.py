from django.db import models
from .user import StudentData

class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    batchName = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    batchStatus = models.BooleanField("Batch Status", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    batchIncharge = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True, blank=True, related_name='batches')
    teachers = models.ManyToManyField(
        "Teacher", related_name='batch_teachers', blank=True
    )

    def __str__(self):
        return self.batchName
    
    def reorderstudents(self):
        students_in_batch = StudentData.objects.filter(batch=self).order_by(
            "studentName"
        )
        for index, student in enumerate(students_in_batch, start=1):
            student.rollNo = index
            student.save()