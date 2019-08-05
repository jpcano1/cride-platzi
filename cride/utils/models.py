""" Django models utilities """

# Django models
from django.db import models


class CRideModel(models.Model):
    """ Comparte Ride base model.

        CRidemodel acts as an abstract base class from whick every
        other model in the project will inherit. Thi class provides
        every table with the following attibutes
         * created (DateTime): Store the datetime the object was created
         * modified (DateTime): Store the las datetime the object was modified
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the objet was created'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )

    class Meta:
        """ Meta opptions"""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']
