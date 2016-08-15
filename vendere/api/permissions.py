from rest_framework import permissions

SAFE_METHODS = ['GET', 'PUT']

class IsAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_superuser:
            return True
        else:
            return False

class IsUserOrReadOnly(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):
        
        return obj.user == request.user