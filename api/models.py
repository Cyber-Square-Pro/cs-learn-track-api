from django.db import models

# Create your models here.
class StudentData(models.Model):
    studentName = models.CharField("Student Name", max_length=30)
    admissionNo = models.IntegerField("Admission Number", unique=True)
    rollNo = models.IntegerField("Roll Number")
    studentClass = models.CharField("Class", max_length=10)
    division = models.CharField("Division", max_length=10)
    gender = models.CharField("Gender", max_length=10)
    fatherName = models.CharField("Father's Name", max_length=30)
    email = models.EmailField("Email", unique=True)
    contactNo = models.CharField("Contact Number", max_length=15)
    joinedDate = models.DateField("Joined Date")
    accountStatus = models.BooleanField("Account Status", default=True)
    studentPassword = models.CharField("Student account password", max_length=30)
    batch = models.ForeignKey("Batch", on_delete=models.CASCADE, related_name='students')
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    profilePic = models.ImageField("Profile Picture", upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.studentName

class Batch(models.Model):
    grade = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    seatNumber = models.IntegerField("Number of seats available")
    activeBatch = models.BooleanField("Is the batch active", default=True)
    schedule = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name