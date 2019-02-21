from rest_framework import permissions
from JobFinderWeb.models import Provider

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS: 
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
 
class IsProviderOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_provider == True
        # return request.user and request.user.is_authenticated #and request.user.is_provider
    def has_object_permission(self, request, view, obj):
        return True    
        # return obj.user == request.user

class IsSeekerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_seeker == True
        # return request.user and request.user.is_authenticated #and request.user.is_provider
    def has_object_permission(self, request, view, obj):
        return True
    
    