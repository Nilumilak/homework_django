from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            print(request.user.is_staff, '111111111111111111')
            return True

        if request.user.is_staff:
            print(request.user.is_staff, '22222222222222222222')
            return True

        print(request.user.is_staff, '3333333333333333333333')
        return obj.creator == request.user