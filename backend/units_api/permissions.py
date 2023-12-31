from rest_framework import permissions
import logging

logger = logging.getLogger("debug_to_stdout")


class UserIsOwnerPermission(permissions.BasePermission):
    """Permission that checks if authenticated user is the owner of the object being requested or created"""

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user

    def has_permission(self, request, view):
        # Catch POST requests that have an owner_id that does not match the authenticated user
        if "owner_id" in request.data:
            self.message = f"owner_id field does not match authenticated user id"
            return request.user.id == int(request.data["owner_id"])

        # Fall back to checking if user is authenticated
        return bool(request.user and request.user.is_authenticated)


class IsUserPermission(permissions.BasePermission):
    """Permission that checks if authenticated user is the user being requested"""

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

    def has_permission(self, request, view):
        return request.user.id == int(view.kwargs["pk"])
