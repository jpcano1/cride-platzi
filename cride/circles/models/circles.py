""" Circle Model """

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Circle(CRideModel):
    """ Circle Model
        A circle is a private group where rides are offered and taken
        by its members. To join a circle, a user must receive an unique
        invitation code from an existing circle of member.
    """

    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)

    members = models.ManyToManyField(
        'users.User',
        through='circles.Membership',
        through_fields=('circle', 'user')
    )

    #Stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Verified circles are also know as official communities'
    )

    is_public = models.BooleanField(
        default=True,
        help_text='Public circles are in the main page so everyone know abput their existence'
    )

    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='Limited circles can row up to a fixed number of members'
    )

    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this will be the limit of the number of members'
    )

    def __str__(self):
        """ Returns circle name """
        return self.name

    @staticmethod
    def readCSV():
        """ Lee el archivo .csv de django. """
        lectura = open('cride/circles/models/circles.csv', 'r')
        lineas = lectura.readlines()

        for linea in lineas:
            partes = linea.split(',')
            name = partes[0]
            slug_name = partes[1]
            is_public = True if int(partes[2]) != 0 else False
            # if int(partes[2]) == 0: is_public = False
            verified  = True if int(partes[3]) != 0 else False
            # if int(partes[3]) == 0: verified = False
            is_limited = False if int(partes[4]) == 0 else True
            # if int(partes[4]) > 0: is_limited = True
            members_limit = int(partes[4])

            Circle.objects.create(
                name=name,
                slug_name=slug_name,
                is_public=is_public,
                verified=verified,
                is_limited=is_limited,
                members_limit=members_limit
            )


    class Meta(CRideModel.Meta):
        """ Meta class """
        ordering = ['-rides_taken', '-rides_offered']




