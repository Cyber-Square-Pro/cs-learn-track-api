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


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    sessionName = models.CharField(max_length=50, unique=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sessions')
    createdBy = models.ForeignKey(
        "Teacher", on_delete=models.SET_NULL, null=True, blank=True, related_name='created_sessions'
    )
    startDateTime = models.DateTimeField("Start Date Time")
    endDateTime = models.DateTimeField("End Date Time")

    def __str__(self):
        return self.sessionName


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(StudentData, on_delete=models.CASCADE, related_name='attendances')
    status = models.BooleanField("Attendance Status", default=False)

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student} - {self.session} - {'Present' if self.status else 'Absent'}"