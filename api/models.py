from django.db import models

# Create your models here.
class StudentData(models.Model):
    studentName = models.CharField("Student Name",  max_length=30)

    studentID = models.IntegerField("Student Unique Identifier")
    studentPassword = models.CharField("Student account password", max_length=30)

    def __str__(self):
        return self.studentName

class AdminData(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

