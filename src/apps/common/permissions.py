from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level: safe methods open; writes require ownership.

    Assumes the object exposes an ``owner`` attribute — rename ``owner_field``
    per model.
    """

    owner_field = "owner"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, self.owner_field, None) == request.user
