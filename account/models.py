from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.contrib.contenttypes.fields import GenericRelation
from social.models import Like

class AccountManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Account(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=50, unique=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='account/%Y/%m/%d', blank=True, null=True)

    blog_url = models.URLField(max_length=100, blank=True, null=True)
    facebook_url = models.URLField(max_length=100, blank=True, null=True)
    instagram_url = models.URLField(max_length=100, blank=True, null=True)

    likes = GenericRelation(Like, related_query_name='accounts')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = AccountManager()

    def __str__(self):
        return self.name;

    def get_absolute_url(self):
        return reverse_lazy('account-detail', kwargs={'pk': self.pk})
