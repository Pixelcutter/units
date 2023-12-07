from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id


class IsUserPermission(permissions.BasePermission):
    """Permission that checks if authenticated user is user being requested"""

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
