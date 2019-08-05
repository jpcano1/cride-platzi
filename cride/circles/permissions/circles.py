""" Circles permission classes """

# Django REST Framework
from rest_framework import permissions

# Models
from cride.circles.models import Membership

class IsCircleAdmin(permissions.BasePermission):
    """ Allow Access only to circle admins """

    def has_object_permission(self, request, view, obj):
        """ Verify user have a membership in the object """
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True


