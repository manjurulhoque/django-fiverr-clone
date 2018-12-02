from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=500, null=True)
    about = models.CharField(max_length=1000, null=True)
    slogan = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.user.username


class Gig(models.Model):
    CATEGORY_CHOICES = (
        ("GD", "Graphics & Design"),
        ("DM", "Digital & Marketing"),
        ("VA", "Video & Animation"),
        ("MA", "Music & Audio"),
        ("PT", "Programming & Tech")
    )

    title = models.CharField(max_length=500)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=1000)
    price = models.IntegerField(default=6)
    photo = models.FileField(upload_to='gigs')
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete='cascade')
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    gig = models.ForeignKey(Gig, on_delete='cascade')
    buyer = models.ForeignKey(User, on_delete='cascade')
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.gig.title


class Review(models.Model):
    gig = models.ForeignKey(Gig, on_delete='cascade')
    user = models.ForeignKey(User, on_delete='cascade')
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.content
