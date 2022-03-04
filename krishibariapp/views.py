from asyncio.windows_events import NULL
from fileinput import filename
import json
from multiprocessing import context
from pyexpat import model
from django.db.models import Count
import re
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login,logout
from django.http import Http404, JsonResponse
from django.shortcuts import  redirect, render
from .models import Dbtable, allArticles, allCourseVideos, articleComment, coursesList , strawbarryVideoTable
from django.contrib import messages
from .models import videoTable
from django.contrib.auth.decorators import login_required
from .forms import Video_form, add_post,course_add, video_add
from django.views.generic import ListView, DetailView
from .templatetags import extras

# start of sub admin views
@login_required(login_url="/adminLogin")
def my_articles(request):
    form=add_post()
    articles=allArticles.objects.filter(auther=request.user)
    if request.method=='POST':
        form=add_post(request.POST)
        if form.is_valid():
            obj=allArticles()
            obj.title=form.cleaned_data['title']
            obj.auther=request.user
            obj.article=form.cleaned_data['article']
            obj.save()
    return render(request,'subadmintemplates/home/my-articles.html',{'articles':articles,'form': form})
@login_required(login_url="/adminLogin")
def delVideo(request):
    if request.method=='POST':
        idc=request.POST.get('cid')
        pi=allCourseVideos.objects.get(pk=idc)
        pi.delete()
        return JsonResponse({'status':1})
    return JsonResponse({'status':0})
@login_required(login_url="/adminLogin")
def activeState(request):
    if request.method=='POST':
        id=request.POST.get('sid')
        pi=coursesList.objects.get(id=id)
        if pi.active_state==1:
            coursesList.objects.filter(id=id).update(active_state=0)
        else:
            coursesList.objects.filter(id=id).update(active_state=1)
        # print(id)
    return JsonResponse({'status':1})

@login_required(login_url="/adminLogin")
def courseDetails(request):
    one_objs = coursesList.objects.all().prefetch_related('allcoursevideos_set')
    return render(request,'subadmintemplates/home/courseDetails.html',{"one_objs":one_objs})
@login_required(login_url="/adminLogin")
def addVideo(request):
    form=video_add()
    if request.method=='POST':
        form=video_add(data=request.POST,files=request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.course_name=request.POST.get('course_name')
            instance.save()
            messages.info(request,'Successfully Added.')
            form=video_add()
    return render(request,'subadmintemplates/home/addVideo.html',{"form":form})

@login_required(login_url="/adminLogin")
def newCourses(request):
    course_list=coursesList.objects.all()
    form=course_add()
    if request.method=='POST':
        form=course_add(request.POST)
        if form.is_valid():
            if coursesList.objects.filter(course_name=form.cleaned_data['course_name']).exists():
                messages.info(request,'Course is already exists.')
            else:
                form.save()
                messages.success(request,'Successfully Added.')
    return render(request,'subadmintemplates/home/newCourse.html',{"form":form,"course_list":course_list})
@login_required(login_url="/adminLogin")
def userCourses(request):
    video=strawbarryVideoTable.objects.all()
    return render(request,'userCourses.html',{"video":video})

@login_required(login_url="/adminLogin")
def courses(request):
    if request.method=='POST':
        form=Video_form(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Added.')
    else:
        form=Video_form()
    return render(request,'subadmintemplates/home/courses.html',{'form':form})

@login_required(login_url="/adminLogin")
def user_list(request):
    user_list=Dbtable.objects.filter(is_admin=False,is_staff=False,is_subAdmin=False,is_superuser=False).all()
    return render(request,'subadmintemplates/home/userinfo.html',{
        'user_list' : user_list
    })

@login_required(login_url="/adminLogin")
def index(request):
    users=Dbtable.objects.filter(is_admin=False,is_staff=False,is_subAdmin=False,is_superuser=False).all().count()
    courses=coursesList.objects.all().count()
    tvid=allCourseVideos.objects.all().count()
    return render(request,'subadmintemplates/home/index.html',{'user_cnt':users,'courses':courses,'tvid':tvid})

def subadmin(request):
    if request.method=='POST':
        email =request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        #type_obj = user.objects.get(user=user)
        if user :
            if user.is_admin:
                login(request,user)
                return redirect('/subadminhome')
    return render(request,'adminLogin.html')

#end of sub Admin views

# start of user site views
# def alltutorials(request):
#     return render(request,'alltutorials.html')

def showArticlexView(request):
    article_1=allArticles.objects.get(pk=1)
    all=allArticles.objects.all()
    return render(request,'alltutorialsx.html',{'article_1':article_1,'all':all})
def showArticleView(request,pk):
    post=allArticles.objects.get(pk=pk)
    all=allArticles.objects.all()
    comments=articleComment.objects.filter(post=post,parent=None)
    replies=articleComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.pk not in replyDict.keys():
            replyDict[reply.parent.pk]=[reply]
        else:
            replyDict[reply.parent.pk].append(reply)
    context={'post':post, 'all':all,'comments':comments,'user':request.user,'replyDict': replyDict}
    return render(request,'alltutorials.html',context)
def addcomment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= allArticles.objects.get(pk=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno == "":
            comment=articleComment(comment= comment, user=user, post=post)
            comment.save()
        else:
            parent=articleComment.objects.get(pk=parentSno)
            comment=articleComment(comment=comment,user=user,parent=parent,post=post)
            comment.save()
        # messages.success(request, "Your comment has been posted successfully")
    return redirect(f"/{post.pk}")
def homepage(request):
    video=videoTable.objects.all()
    return render(request,'home.html',{"video":video})
def log_out(request):
    logout(request)
    return redirect('/')
def profile(request):
    return render(request,'userProfile.html')
def insertrecord(request):
    if request.method=='POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        perAddress=request.POST['perAddress']
        currAddress=request.POST['currAddress']
        nid=request.POST['NID']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if Dbtable.objects.filter(name=name).exists():
            messages.info(request,'Name taken.')
            return redirect('/register')
        elif Dbtable.objects.filter(email=email).exists():
            messages.info(request,'Email taken.')
            return redirect('/register')
        else:
            user=Dbtable.objects.create_user(email=email,name=name,phone=phone,perAddress=perAddress,currAddress=currAddress,nid=nid,password=password1)
            user.save()
            user1 = authenticate(email=email,name=name, password=password1)
            login(request, user1)
            return redirect('/')
    return render(request,'register.html')
def log_in(request):
    if request.method == 'POST':
        name = request.POST['name']
        email =request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            #messages.success(request,'login successful')
            return redirect('/')
            # Redirect to a success page....
        else:
            messages.info(request,'invalid user')
            return redirect('/login')
            # Return an 'invalid login' error message....
    else: return render(request,'login.html')

def home(request):
    return render(request,'home.html',{'name':"Faiaz"})

def coursesite(request):
    return render(request,'coursesite.html')
def onlineCourses(request):
    return render(request,'onlineCourses.html')