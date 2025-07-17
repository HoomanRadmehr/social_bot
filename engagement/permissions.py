# engagement/permissions.py

from rest_framework import permissions
from .models import Profile, Alert

class IsOwnerPermission(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Profile):
            return obj.creator == request.user
        elif isinstance(obj, Alert):
            return obj.profile.creator == request.user
        return False
