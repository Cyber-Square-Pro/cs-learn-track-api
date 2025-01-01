from rest_framework.permissions import BasePermission
from api.models import UserProfile

class isTeacher(BasePermission):
    def has_permission(self, request, view):
        if not request.user.id:
            return False
        
        userProfile = UserProfile.objects.get(user_id=request.user.id)

        return userProfile.role == 'teacher'

class isStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.id:
            return False
        
        userProfile = UserProfile.objects.get(user_id=request.user.id)

        return userProfile.role == 'student'
