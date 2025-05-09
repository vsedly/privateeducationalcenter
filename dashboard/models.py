from django.db import models

# For custom user things
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings


# Create your models here.
class Notes(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='Notes'
        verbose_name_plural='Notes'
        
        
        
        
class Homework(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)
    
    def __str__(self):
        return self.subject
    
class Todo(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    is_finished=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    


# class UserManager(BaseUserManager):
#     def create_user(self,email,password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set.')
#         email=self.normalize_email(email)
#         user=self.model(email=email,**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
        
        
#     def create_superuser(self,email password=None):
#         user = self.create_user(
#             email=self.model(email)
            
          
#         )
#         # Set superuser-specific fields
#         user.is_admin = True
#         user.is_active = True
#         user.is_superadmin = True
#         user.is_staff = True
#         user.save(using=self._db)  
#         return user


# class User(AbstractBaseUser):
#     GENDER = (
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Others', 'Others')
#     )

#     # Basic user fields
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(max_length=100, unique=True)

#     gender = models.CharField(max_length=10, choices=GENDER)

#     # Required fields
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)  
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#     is_superadmin = models.BooleanField(default=False)

#     # Custom manager for user creation
#     objects = UserManager()

#     # Authentication settings
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

#     def __str__(self):
#         return self.email

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'



# def has_perm(self,perm,obj=None):
#     return self.is_admin

# def has_module(self,app_label):
#     return True

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('the email field must be set')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
             raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email,password,**extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    # username = models.CharField(max_length=100, unique=True)
    fullname=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)
    

    objects=CustomUserManager()
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['fullname','password']
    
    def __str__(self):
        return self.email


    
        
    
        
        
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    
    
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self.create_user(email, password, **extra_fields)
            
# class CustomUser(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     fullname = models.CharField(max_length=100)
#     promo_code = models.CharField(max_length=25, blank=True)
#     is_active = models.BooleanField(default=True) #Change while integration Payment Gateway
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['fullname']

#     def __str__(self):
#         return self.email

