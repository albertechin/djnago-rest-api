from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, email, name, password=None):
        """Creates a new user profle object."""

        if not email:
            raise ValueError('User must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with given details"""

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a user model"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get the full name of the user"""

        return self.name

    def get_short_name(self):
        """Used to get the short name of the user"""

        return self.name

    def __str__(self):
        """Django uses this function to convert th object to string"""

        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length = 255)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        """return the model as a string."""

        return self.status_text

class UserLocation(models.Model):
    """User locations"""
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    lat = models.CharField(max_length = 15)
    lng = models.CharField(max_length = 15)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        """return the model as a string."""
        location = "lat: "+self.lat+"; lng: "+self.lng
        return location


