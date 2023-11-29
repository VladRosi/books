from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCreatorOrStaffOrReadOnly(BasePermission):
  def has_object_permission(self, request, view, obj):
    return bool((request.method in SAFE_METHODS) \
      or (request.user and request.user.is_authenticated and request.user == obj.creator) \
      or (request.user.is_staff)
      )
