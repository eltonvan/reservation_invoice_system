from rest_framework import permissions


class CanCreateUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser is False:
            return False
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):


        if request.user.is_superuser:
            print("superuser")
            return True
        # refers to CutomUser model - logged in username returns True
        elif hasattr(obj, "username") and obj.pk == request.user.pk:
            print("first condition")
            return request.user.is_superuser or obj.username == request.user.username
        # refers to other models that all contain user attribute
        #  - logged in username returns True
        elif hasattr(obj, "user") and obj.reservation == request.user:
            print("second condition")
            return request.user.is_superuser or obj.reservation.user == request.user

        else:
            print("third condition")
            return False
