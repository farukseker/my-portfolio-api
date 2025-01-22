from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Testimonial(models.Model):
    message = models.CharField(max_length=500)
    name = models.CharField(max_length=75)
    title = models.CharField(max_length=75)

    photo = models.URLField(default='', blank=True, null=True)

    phone = PhoneNumberField(default='', blank=True, null=True)
    email = models.EmailField(default='', blank=True, null=True)

    instagram = models.URLField(default='', blank=True, null=True)
    github = models.URLField(default='', blank=True, null=True)
    twitter = models.URLField(default='', blank=True, null=True)
    stackoverflow = models.URLField(default='', blank=True, null=True)
    linkedin = models.URLField(default='', blank=True, null=True)
    youtube = models.URLField(default='', blank=True, null=True)

    approved = models.BooleanField(default=False)

