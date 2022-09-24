from distutils.command.upload import upload
import email
from operator import truediv
from pickle import TRUE
from pydoc import visiblename
from pyexpat import model
from sys import stdout
from tokenize import blank_re
from turtle import title
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.forms import CharField
from ckeditor.fields import RichTextField
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField
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
    profile_pic=models.ImageField(upload_to='images/', default='images/profile-icon.png')
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

class onlineCourseList(models.Model):
    about=models.CharField(max_length=1000000,null=True,blank=True)
    course_name=models.CharField(max_length=255,unique=True)
    course_description=models.TextField(blank=True)
    course_overview=models.TextField(blank=True)
    course_overview_image=models.ImageField(upload_to='images/', default='images/default.jpg')
    learning_objectives=models.TextField(blank=True)
    price=models.IntegerField(default=0)
    instructor=models.ForeignKey(Dbtable, on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    active_state=models.BooleanField(default=False)
    def __str__(self):
        return self.course_name

class liveCourseList(models.Model):
    about=models.CharField(max_length=1000000,null=True,blank=True)
    live_course_name=models.CharField(max_length=255,unique=True)
    course_description=models.TextField(blank=True)
    course_overview=models.TextField(blank=True)
    course_overview_image=models.ImageField(upload_to='images/', default='images/default.jpg')
    learning_objectives=models.TextField(blank=True)
    price=models.IntegerField(default=0)
    instructor=models.ForeignKey(Dbtable, on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
    videoSessionLink=models.URLField(blank=True,null=True)
    def __str__(self):
        return self.live_course_name

class onlineCourseStudents(models.Model):
    course=models.ForeignKey(onlineCourseList,on_delete=models.CASCADE)
    student=models.ForeignKey(Dbtable,on_delete=models.CASCADE)
    transection_id=models.TextField(max_length=30,null=True)
    status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.student.name) + ' | ' + str(self.course)
        
class liveCourseStudents(models.Model):
    course=models.ForeignKey(liveCourseList,on_delete=models.CASCADE)
    student=models.ForeignKey(Dbtable,on_delete=models.CASCADE)
    transection_id=models.TextField(max_length=100,null=True,blank=True)
    status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.student.name) + ' | ' + str(self.course)

DIFF_CHOICES = {
    ('easy','easy'),
    ('medium','medium'),
    ('hard','hard'),
}

class course_exam(models.Model):
    title=models.CharField(max_length=50)
    course=models.ForeignKey(onlineCourseList,on_delete=models.CASCADE)
    number_of_questions=models.IntegerField()
    time=models.IntegerField(help_text="duration of the exam in minutes")
    required_score_to_pass= models.IntegerField(help_text="required score to pass")
    difficulty=models.CharField(max_length=6,choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.title}-{self.course}"

    def get_questions(self):
        return self.course_exam_question_set.all()

class course_exam_question(models.Model):
    text=models.CharField(max_length=100)
    exam=models.ForeignKey(course_exam,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.course_exam_answer_set.all()

class course_exam_answer(models.Model):
    text=models.CharField(max_length=100)
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(course_exam_question,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

class course_exam_result(models.Model):
    exam=models.ForeignKey(course_exam,on_delete=models.CASCADE)
    user=models.ForeignKey(Dbtable,on_delete=models.CASCADE)
    score=models.FloatField()

    def __str__(self):
        return str(self.pk)



class allCourseVideos(models.Model):
    name=models.ForeignKey(onlineCourseList,on_delete=models.CASCADE,blank=True)
    caption=models.CharField(max_length=100,blank=True,null=True)
    video=models.FileField(upload_to="video/%y",blank=True)
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
    article=RichTextUploadingField(blank=True,null=True)
    def __str__(self) :
        return self.title +' | '+ str(self.auther.name)
class articleComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(Dbtable, on_delete=models.CASCADE)
    post=models.ForeignKey(allArticles,related_name='comments', on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)
class allBlogs(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    auther=models.ForeignKey(Dbtable,on_delete=models.CASCADE)
    blog_overview=models.TextField(blank=True)
    blog_image=models.ImageField(upload_to='images/', default='images/default.jpg')
    the_blog=RichTextUploadingField(blank=True,null=True)
    likes=models.ManyToManyField(Dbtable, related_name='likes',blank=True,null=True)
    dislikes=models.ManyToManyField(Dbtable,related_name='dislikes',blank=True,null=True)
    bookmark=models.ManyToManyField(Dbtable,related_name='bookmark',blank=True,null=True)
    def __str__(self) :
        return self.title

class allquestion(models.Model):
    title=models.CharField(max_length=255)
    auther=models.ForeignKey(Dbtable,on_delete=models.CASCADE)
    question=RichTextUploadingField(blank=True,null=True)
    approved=models.BooleanField(default=False)
    timestamp= models.DateTimeField(default=now)
    def __str__(self):
        return self.title

    def get_all_answers(self):
        return self.question_answer_set.all()
    def get_answer_count(self):
        return self.question_answer_set.all().count()

class question_answer(models.Model):
    answer=RichTextUploadingField()
    auther=models.ForeignKey(Dbtable,on_delete=models.CASCADE)
    question=models.ForeignKey(allquestion,on_delete=models.CASCADE)
    like=models.ManyToManyField(Dbtable,related_name='answer_like', blank=True,null=True)
    dislike=models.ManyToManyField(Dbtable,related_name='answer_dislike',blank=True,null=True)
    timestamp=models.DateTimeField(default=now)
    def __str__(self):
        return self.question + ' ' + str(self.auther.name)+ ' '+str(self.timestamp)
