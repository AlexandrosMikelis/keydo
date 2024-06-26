import uuid
from django.db import models

from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('A password is required.')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password):
        
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
class UserKeystrokes(models.Model):
    
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    keystroke_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_code = models.CharField(max_length=15)
    event = models.CharField(max_length=15)
    timestamp = models.CharField(max_length=30)