from pyexpat import model
from tokenize import blank_re
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.forms import CharField
from ckeditor.fields import RichTextField
from django.utils.timezone import now
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
        return True

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    # @property
    # def is_staff(self):
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

class videoTable(models.Model):
    video=models.FileField(upload_to="video/%y")

class coursesList(models.Model):
    course_name=models.CharField(max_length=100,unique=True)
    active_state=models.BooleanField(default=False)
    def __str__(self):
        return self.course_name
class allCourseVideos(models.Model):
    name=models.ForeignKey(coursesList,on_delete=models.CASCADE)
    caption=models.CharField(max_length=100)
    video=models.FileField(upload_to="video/%y")
    is_paid=models.BooleanField(default=False)
    def __str__(self):
        return self.caption

class strawbarryVideoTable(models.Model):
    caption=models.CharField(max_length=100)
    video=models.FileField(upload_to="video/%y")
    is_paid=models.BooleanField(default=False)
    def __str__(self):
        return self.caption

class allArticles(models.Model):
    title=models.CharField(max_length=255)
    auther=models.ForeignKey(Dbtable,on_delete=models.CASCADE)
    article=RichTextField(blank=True,null=True)
    def __str__(self) :
        return self.title +' | '+ str(self.auther.name)
class articleComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(Dbtable, on_delete=models.CASCADE)
    post=models.ForeignKey(allArticles,related_name='comments', on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)