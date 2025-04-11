from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_administrator', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    iin = models.CharField(max_length=12, unique=True, verbose_name="Individual Identification Number", blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", 
        default="profile_pictures/default.png",
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    is_administrator = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'iin']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    # get full name
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


# class TelegramUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     telegram_id = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return f"{self.user.username} - Telegram ID: {self.telegram_id}"

# class TelegramUser(models.Model):
#     user = models.OneToOneField(
#         User, 
#         on_delete=models.CASCADE,
#         related_name='telegram_user'
#     )
#     telegram_id = models.BigIntegerField(unique=True)

#     def __str__(self):
#         return f"TelegramUser for {self.user.get_full_name()}"


# class TelegramConnectionToken(models.Model):
#     user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
#     token = models.CharField(max_length=36, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)

#     def __init__(self, *args, **kwargs):
#         if 'token' not in kwargs:
#             kwargs['token'] = uuid.uuid4().hex
#         super().__init__(*args, **kwargs)

#     def is_valid(self):
#         """Check if the token is unused and not older than 10 minutes."""
#         return not self.is_used and (timezone.now() - self.created_at).total_seconds() < 600

#     def __str__(self):
#         return f"Token for {self.user.get_full_name()}"
