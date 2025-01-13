from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	ROLE_CHOICES = (
		('student', 'Student'),
		('teacher', 'Teacher'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	role = models.CharField("Role", max_length=10, choices=ROLE_CHOICES)
	dbUniqueID = models.IntegerField("database Unique ID")
	active = models.BooleanField("Active", default=False)
	last_login = models.DateTimeField("Last Login", auto_now=True)

	def __str__(self):
		return f"{self.user.username} ({self.role})"


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

class Teacher(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField("Name", max_length=50)
	email = models.EmailField("Email", unique=True)
	subject = models.CharField("Subject", max_length=50)
	hireDate = models.DateField("Hire Date")
	contactNo = models.CharField("Contact Number", max_length=15)
	teacherPassword = models.CharField("Teacher Password", max_length=100)
	profilePic = models.ImageField("Profile Picture", upload_to='profile_pictures/', blank=True, null=True)

	def __str__(self):
		return self.name