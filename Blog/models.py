import time
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


@python_2_unicode_compatible
class Manager(BaseUserManager):
    def create_user(self, email, password=None):
        new_user = self.model(
            email=self.normalize_email(email)
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(self, email, password):
        new_admin_user = self.create_user(
            email=email,
            password=password
        )
        new_admin_user.is_admin = True
        new_admin_user.save(using=self._db)
        return new_admin_user


@python_2_unicode_compatible
class User(AbstractBaseUser):
    id = models.CharField(max_length=50, default=next_id(), primary_key=True)

    name = models.CharField(max_length=50, null=True)
    image = models.CharField(max_length=500, null=True)
    email = models.CharField(max_length=50, unique=True)

    password = models.CharField(max_length=500, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=False, name='active')
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = Manager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return "User " + self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


@python_2_unicode_compatible
class Blog(models.Model):
    id = models.CharField(max_length=50, default=next_id(), primary_key=True)
    user_id = models.CharField(max_length=50, null=True)
    user_name = models.CharField(max_length=50, null=True)
    user_image = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=50, null=True)
    summary = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Blog " + self.name


@python_2_unicode_compatible
class Comment(models.Model):
    id = models.CharField(max_length=50, default=next_id(), primary_key=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=50, null=True)
    user_name = models.CharField(max_length=50, null=True)
    user_image = models.CharField(max_length=500, null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Comment on " + " : " + self.user_id
