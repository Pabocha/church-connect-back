from django.db import models
from django.contrib.auth.models import BaseUserManager, Group, AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import os
from django.core.exceptions import ValidationError

# Create your models here.

class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='group_profile')
    image = models.ImageField(upload_to='group_images/', blank=True, null=True)

    def __str__(self):
        return self.group.name


def rename_img(instance, filename):
    upload_to = "media/"
    extension = filename.split(".")[-1]
    if instance.first_name:
        name = instance.first_name.lower().replace(' ', '_')
        filename = (f"profile/{name}.{extension}")
        return os.path.join(upload_to, filename)

phone_validator = RegexValidator(
    r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$",
    "The phone number provided is invalid"
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field is required'))
        if not phone_number:
            raise ValueError(_('The Phone number field is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('The Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('The Superuser must have is_superuser=True.'))
        
        return self.create_user(email, phone_number, password, **extra_fields)

class Members(AbstractBaseUser):
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set'  # utilisez un nom personnalisé ici
    )
    groups = models.ManyToManyField(Group, blank=True, related_name='user_groups')
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, validators=[phone_validator], unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    image = models.ImageField(upload_to=rename_img, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
