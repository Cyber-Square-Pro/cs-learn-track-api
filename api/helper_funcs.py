from django.contrib.auth.models import User
from api.models import UserProfile

def create_user(username, password, email, role):
    # Create a new User instance
    user = User.objects.create_user(username=username, password=password, email=email)

    # Update the role in the UserProfile
    UserProfile.objects.create(user=user, role=role)
