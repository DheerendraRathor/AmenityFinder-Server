from django.db import models


class Amenity(models.Model):
    name = models.CharField(max_length=64)
    icon = models.ImageField()

    class Meta:
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return self.name