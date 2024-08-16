from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.utils.translation import gettext as _

class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    email = models.EmailField(_("Email"), unique=True, max_length=50, blank=True)
    username = models.CharField(_("Username"), unique=True, max_length=50, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, null=True, blank=True)
    is_verified = models.BooleanField(_("Is Verified"), default=False)
    objects = CustomUserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.get_full_name() or self.email
    

    




