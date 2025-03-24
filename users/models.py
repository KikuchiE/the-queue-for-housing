from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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

# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class UserManager(BaseUserManager):
#     def create_user(self, password=None, **extra_fields):
#         extra_fields.setdefault('is_active', True)
#         user = self.model(**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     iin = models.CharField(max_length=12, unique=True, verbose_name="Individual Identification Number", blank=True, null=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     email = models.EmailField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255, blank=True)
#     last_name = models.CharField(max_length=255, blank=True)
#     middle_name = models.CharField(max_length=255, blank=True, null=True)
    
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)

#     objects = UserManager()
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email