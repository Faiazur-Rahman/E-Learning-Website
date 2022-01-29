from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email,name,phone,perAddress,currAddress,nid,password):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        if not phone:
            raise ValueError('Users must have a phone number')
        if not perAddress:
            raise ValueError('Users must have permanent address')
        if not currAddress:
            raise ValueError('Users must have current address')
        user = self.model(
            name=name,
            phone=phone,
            email=self.normalize_email(email),
            perAddress=perAddress,
            currAddress=currAddress,
            NID=nid,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name,phone,perAddress,currAddress,NID,password):
        user = self.create_user(
            name=name,
            phone=phone,
            email=self.normalize_email(email),
            perAddress=perAddress,
            currAddress=currAddress,
            nid=NID,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_subAdmin=True
        user.save(using=self._db)
        return user
class Dbtable(AbstractBaseUser,PermissionsMixin):
    name=models.TextField(max_length=100)
    phone=models.TextField( max_length=15)
    email=models.EmailField(max_length=60,unique=True)
    perAddress=models.TextField( max_length=100)
    currAddress=models.TextField( max_length=100)
    NID=models.TextField(max_length=100)
    password=models.TextField(max_length=100)
    # email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= None
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_subAdmin             = models.BooleanField(default=False)
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone','perAddress','currAddress','NID','password']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

class videoTable(models.Model):
    video=models.FileField(upload_to="video/%y")
