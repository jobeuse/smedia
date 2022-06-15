from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class userProfile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, verbose_name="user", related_name="profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    picture = models.ImageField(
        upload_to='uploads/profile_pictures', blank=True)
   # picture =models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
