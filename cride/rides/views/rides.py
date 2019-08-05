""" Rides views """

# Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Serializer
from cride.rides.serializers import (CreateRideSerializer,
                                     RideModelSerializer,
                                     JoinRideSerializer,
                                     EndRideSerializer,
                                     CreateRideRatingSerializer)

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsActiveCircleMember
from cride.rides.permissions import IsRideOwner, IsNotRideOwner

# Filter
from rest_framework.filters import SearchFilter, OrderingFilter

# Models
from cride.circles.models import Circle

# Utilities
from django.utils import timezone
from datetime import timedelta

class RideViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin):
    """ Rides Viewset """

    serializer_class = CreateRideSerializer
    permission_classes = [IsAuthenticated, IsActiveCircleMember]
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('departure_date', 'arrival_date', 'available_seats')
    ordering_fields = ('departure_date', 'arrival_date', 'available_seats')
    search_fields = ('departure_location', 'arrival_location')

    def dispatch(self, request, *args, **kwargs):
        """ Verify that the circle exists """
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """ Assign permission based on action """
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update', 'finish']:
            permissions.append(IsRideOwner)
        if self.action in ['join']:
            permissions.append(IsNotRideOwner)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """ Add circle to serializer context """
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def get_serializer_class(self):
        """ Return serializer base on action """
        if self.action == 'create':
            return CreateRideSerializer
        if self.action == 'update':
            return JoinRideSerializer
        if self.action == 'finish':
            return EndRideSerializer
        if self.action == 'rate':
            return CreateRideRatingSerializer
        return RideModelSerializer

    def get_queryset(self):
        """ Return active circle's rides. """
        if self.action != 'finish':
            offset = timezone.now() + timedelta(minutes=10)
            return self.circle.ride_set.filter(
                departure_date__gte=offset,
                available_seats__gte=1,
                is_active=True
            )
        return self.circle.ride_set.all()

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        """ Add reqeusting user to ride. """
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={'passenger': request.user.pk},
            context={'ride': ride, 'circle': self.circle},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        """ Call by owners to finish the ride """
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={'is_active': False, 'current_time': timezone.now()},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def rate(self, request, *args, **kwargs):
        """ Rate Ride """
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['ride'] = ride
        serializer = serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_201_CREATED)
