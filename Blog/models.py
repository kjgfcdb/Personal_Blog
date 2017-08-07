import time
import uuid

from django.contrib.auth.models import User, AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


@python_2_unicode_compatible
class User(AbstractBaseUser):
    id = models.CharField(max_length=50, default=next_id(), primary_key=True)
    email = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50, null=True)
    admin = models.NullBooleanField()
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False,name='active')
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return "User " + self.name


@python_2_unicode_compatible
class Blog(models.Model):
    id = models.CharField(max_length=50, default=next_id(), primary_key=True)
    user_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    user_image = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    summary = models.CharField(max_length=200)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Blog " + self.name


@python_2_unicode_compatible
class Comment(models.Model):
    id = models.CharField(max_length=50, default=next_id(), primary_key=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    user_image = models.CharField(max_length=500)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Comment on " + " : " + self.user_id
