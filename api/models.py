from django.db import models

# Create your models here.
class StudentData(models.Model):
    studentName = models.CharField("Student Name",  max_length=30)
    studentID = models.IntegerField("Student Unique Identifier", unique=True)
    studentPassword = models.CharField("Student account password", max_length=30)
    studentBatch = models.ForeignKey("Batch", on_delete=models.CASCADE, related_name='students')
    studentPFP = models.ImageField("Student Profile Picture", upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.studentName

class Batch(models.Model): # CLass teacher as foreign key
    grade = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    seat_number = models.IntegerField("Number of seats available")

    active_batch = models.BooleanField("Is the batch active", default=True)
    schedule = models.TextField()  # Ask about it, unsure how to implement
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name