from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    currency = models.CharField(max_length=50)
    country_pic = models.FileField(default='')

    def __str__(self):
        return self.name + " - " + self.language + " - " + self.currency


class University(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    university_name = models.CharField(max_length=1000)
    state = models.CharField(max_length=250)
    rank = models.IntegerField()
    intro_video = models.CharField(max_length=1000, blank=True)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.university_name + " - " + self.state

