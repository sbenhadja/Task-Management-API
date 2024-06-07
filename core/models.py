from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):

    #use_in_migration = True

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit posséder un email")
        user = self.model(
            email=self.normalize_email(email), 
            first_name = first_name,
            last_name = last_name,
            **extra_fields)
    
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit posséder un email")        
        user = self.model(email=self.normalize_email(email), 
            first_name = first_name,
            last_name = last_name,
            **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    