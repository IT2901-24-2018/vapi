from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create and edit.
    Read only for normal users and unauthorized users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class IsStaffOrCreateOnly(permissions.BasePermission):
    """
    Custom permission to only allow create and list actions.
    """
    def has_permission(self, request, view):
        # Defining available request methods.
        staff_methods = ("GET", "OPTIONS", "HEAD", "POST")
        not_staff_methods = ("OPTIONS", "POST")

        if request.user.is_staff and request.method in staff_methods:
            # If the user is staff and the request method is among the allowed methods for staff.
            return True
        elif (not request.user.is_staff) and request.method in not_staff_methods:
            # If the user is not staff, but the method is among the allowed for users that are not staff.
            return True
        return False
