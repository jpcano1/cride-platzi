""" Ratings model """

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel

class Rating(CRideModel):
    """ Ride rating
        rates are entities that store the rating a user
        gave to a ride, it ranges from 1 to 5 and it affects
        the ride offerer's overall reputation.
     """

    ride = models.ForeignKey(
        'rides.Ride',
        on_delete=models.CASCADE,
        related_name='rated_ride'
    )
    circle = models.ForeignKey(
        'circles.Circle',
        on_delete=models.CASCADE,
    )

    rating_user = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        help_text='User that emits the rating',
        related_name='rating_user'
    )
    
    rated_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text='User that receives the rating',
        related_name='rated_user'
    )

    comments = models.TextField(blank=True)

    rating = models.FloatField(default=1)

    def __str__(self):
        """ Return Summary """
        return "{} is your calification".format(self.rating)


