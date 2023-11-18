from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
        
    

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a post.
        #return request.is_superuser or obj.user == request.user
    

        return request.user.is_superuser or obj.user == request.user
