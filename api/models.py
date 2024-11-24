from django.db import models

# Create your models here.
class StudentData(models.Model):
    studentName = models.CharField("Student Name",  max_length=30)

    studentID = models.IntegerField("Student Unique Identifier")
    studentPassword = models.CharField("Student account password", max_length=30)

    def __str__(self):
        return self.studentName

class Batch(models.Model):
    name = models.CharField(max_length=100)
    schedule = models.TextField()  # Ask about it, unsure how to implement
    description = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    students = models.ManyToManyField(StudentData, related_name='batches')

    def __str__(self):
        return self.name