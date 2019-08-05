""" IRdes permissions """

# Django REST Framework
from rest_framework.permissions import BasePermission

class IsRideOwner(BasePermission):
    """ Verify requesting is the ride created. """

    def has_object_permission(self, request, view, obj):
        """ Verify requesting user is the right creator """
        return request.user == obj.offered_by

class IsNotRideOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        """ Verify requesting user is the right creator """
        return not request.user == obj.offered_by
