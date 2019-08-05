""" Circle Serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):
    """ Cirlce model serializer """

    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000
    )
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """ Meta Class """

        model = Circle
        fields = (
            'name', 'slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'verified', 'is_public',
            'is_limited', 'members_limit'
        )
        read_only_fields = (
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken'
        )

    def validate(self, data):
        """ Ensure both members limit and is_limited are present. """
        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circle is limites, a member limit must be provided')
        return data
