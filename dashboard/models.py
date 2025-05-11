from django.db import models
from django.conf import settings



from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings



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


class StudentSchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject} ({self.date})"

    class Meta:
        verbose_name = "Student Schedule"
        verbose_name_plural = "Student Schedules"