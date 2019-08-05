""" USers permissions """

# Django REST framework
from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    """ Allow access aonly to objects owned by the requesting user. """

    def has_object_permission(self, request, view, obj):
        """ Check obj and user are the same """
        return request.user == obj
