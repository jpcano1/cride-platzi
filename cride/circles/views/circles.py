""" Circle Views """

# Django REST Framework
from rest_framework import viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsCircleAdmin

# Models
from cride.circles.models import Circle, Membership

# Serializers
from cride.circles.serializers.circles import CircleModelSerializer

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

class CircleViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin):
    """ Circle view set """

    # queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'
    # permission_classes = (IsAuthenticated, )

    # Filters
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'member_limit')
    ordering = ('-members__count', '-rides_offered', '-rides_taken')

    def get_queryset(self):
        """ Restrict list to public-only """
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)

        return queryset

    def get_permissions(self):
        """ Assign permissions based on action. """
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """ Assign Circle member """
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )


