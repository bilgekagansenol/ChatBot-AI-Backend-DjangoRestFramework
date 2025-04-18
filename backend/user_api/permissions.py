from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """allow users to edit their  own profile"""
    def has_object_permission(self, request, view, obj):
        """check user is trying to edit their own profile"""   
        return obj.id == request.user.id
    


