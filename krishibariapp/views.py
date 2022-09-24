from ast import Pass
from asyncio.windows_events import NULL
from codecs import readbuffer_encode
from dis import Instruction
from fileinput import filename
import json
from multiprocessing import context
from operator import truediv
from pyexpat import model
from unicodedata import name
from django.db.models import Count
import re
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login,logout
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import  redirect, render
from .models import *
from django.contrib import messages
from .models import videoTable
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.generic import ListView, DetailView
from .templatetags import extras
import math 
from django.core.mail import send_mail

#start of instructor
def instructor_login(request):
    return render(request,'instructorLogin.html')
def instructor_home(request):
    return render(request,'instructor-home.html')
def instructor_course(request):
    all=onlineCourseList.objects.filter(instructor=request.user)
    return render(request,'instructor-courses.html',{'all':all})
def instructor_the_course(request,pk):
    course=onlineCourseList.objects.get(pk=pk)
    course_vid=allCourseVideos.objects.filter(name=course).exclude(video='')
    form=video_add()
    if request.method=='POST':
        form=video_add(data=request.POST,files=request.FILES)
        if form.is_valid():
            obj=allCourseVideos()
            obj.name=course
            obj.caption=form.cleaned_data['caption']
            obj.video=form.cleaned_data['video']
            obj.is_paid=form.cleaned_data['is_paid']
            obj.save()
            messages.info(request,'Successfully Added.')
            form=video_add()
    return render(request,'instructor-the-course.html',{'course_vid':course_vid,'course':course,'form':form})
# start of sub admin views
def pending_to_active(request,course_pk,stu_pk,sid):
    if sid == 1:
        onlineCourseStudents.objects.filter(pk=stu_pk).update(status=True)
        return redirect('the-course-admin', pk= course_pk)
    else:
        liveCourseStudents.objects.filter(pk=stu_pk).update(status=True)
        return redirect('the-live-course-admin', pk= course_pk)
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
        pi=onlineCourseList.objects.get(pk=id)
        if pi.active_state==1:
            onlineCourseList.objects.filter(pk=id).update(active_state=0)
        else:
            onlineCourseList.objects.filter(pk=id).update(active_state=1)
        # print(id)
    return JsonResponse({'status':1})

@login_required(login_url="/adminLogin")
def courseDetails(request):
    all = onlineCourseList.objects.all()
    #.prefetch_related('allcoursevideos_set')
    return render(request,'subadmintemplates/home/courseDetails.html',{"all":all})
@login_required(login_url="/adminLogin")
def liveCourseDetails(request):
    all= liveCourseList.objects.all()
    return render(request,'subadmintemplates/home/liveCourseDetails.html',{"all":all})
@login_required(login_url="/adminLogin")
def the_course_admin(request,pk):
    course=onlineCourseList.objects.get(pk=pk)
    active_students=onlineCourseStudents.objects.filter(course=course, status=True)
    pending_students=onlineCourseStudents.objects.filter(course=course,status=False)
    course_vid=allCourseVideos.objects.filter(name=course).exclude(video='')
    form1=course_instructor()
    form2=video_add()
    if request.method=='POST':
        form1 =course_instructor(request.POST)
        if form1.is_valid():
            instructor=form1.cleaned_data['instructor']
            onlineCourseList.objects.filter(pk=pk).update(instructor=instructor)
            print(instructor)
        form2=video_add(data=request.POST,files=request.FILES)
        if form2.is_valid():
            obj=allCourseVideos()
            obj.name=course
            obj.caption=form2.cleaned_data['caption']
            obj.video=form2.cleaned_data['video']
            obj.is_paid=form2.cleaned_data['is_paid']
            obj.save()
            messages.info(request,'Successfully Added.')
            form2=video_add()
    online=1
    return render(request,'subadmintemplates/home/the-course.html',{'online':online,'course_vid':course_vid,'pending_students':pending_students,'students':active_students,'course':course,'form1':form1,'form2':form2})
@login_required(login_url="/adminLogin")
def the_live_course_admin(request,pk):
    course=liveCourseList.objects.get(pk=pk)
    active_students=liveCourseStudents.objects.filter(course=course, status=True)
    pending_students=liveCourseStudents.objects.filter(course=course,status=False)
    session_link=0
    if request.method=='POST':
        session_link=request.POST.get('session_url')
        liveCourseList.objects.filter(pk=pk).update(videoSessionLink=session_link)
    online=0
    session_link=course.videoSessionLink
    return render(request,'subadmintemplates/home/the-course.html',{'session_link':session_link,'online':online,'pending_students':pending_students,'students':active_students,'course':course})

@login_required(login_url="/adminLogin")
def liveCourseLinkSend(request,course_pk):
    course=liveCourseList.objects.get(pk=course_pk)
    recievers = []
    for user in liveCourseStudents.objects.filter(status=True):
        recievers.append(user.student.email)
    subject=str(course.live_course_name)+" Live session link."
    message=str(course.live_course_name)+" You are requested to join this live class."
    message+="\n the Link: "+ course.videoSessionLink
    send_mail(subject, message,'faiaz2k20@gmail.com', recievers)

    return redirect('the-live-course-admin', pk= course_pk)
@login_required(login_url="/adminLogin")
def newCourses(request):
    course_list=onlineCourseList.objects.all()
    form=course_add()
    if request.method=='POST':
        form=course_add(request.POST, request.FILES)
        if form.is_valid():
            if onlineCourseList.objects.filter(course_name=form.cleaned_data['course_name']).exists():
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
    courses=onlineCourseList.objects.all().count()
    tvid=allCourseVideos.objects.all().exclude(video='').count()
    return render(request,'subadmintemplates/home/index.html',{'user_cnt':users,'courses':courses,'tvid':tvid})

@login_required(login_url="/adminLogin")
def question_admin(request):
    if request.method=='POST':
        id=request.POST['id']
        action=request.POST['approve']
        if action=='Approve':
            allquestion.objects.filter(pk=id).update(approved=True)
        else:
            pi=allquestion.objects.get(pk=id)
            pi.delete()
    not_approved_questions=allquestion.objects.filter(approved=False).order_by('-timestamp')
    return render(request,'subadmintemplates/home/question-admin.html',{'all':not_approved_questions})
@login_required(login_url="/adminLogin")
def approve_question(request):
    if request.method=='POST':
        id=request.POST.get('cid')
        allquestion.objects.filter(pk=id).update(approved=True)
        return JsonResponse({'status':1})
    return JsonResponse({'status':0})
@login_required(login_url="/adminLogin")
def view_question(request,pk):
    qus=allquestion.objects.get(pk=pk)
    return render(request,'subadmintemplates/home/view-question.html',{'qus':qus})
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

def shofolUddokta(request):
    return render(request,'shofolUddokta.html')

def shofolUddoktaSingle(request):
    return render(request,'shofolUddoktaSingle.html')
def marketPlaces(request):
    return render(request,'marketPlaces.html')

@login_required(login_url="/")
def ownProfile(request):
    user=Dbtable.objects.get(email=request.user.email)
    return render(request,'ownProfile.html',{'user':user})

def course_test_save(request,coursePk):
    if request.method == 'POST':
        questions=[]
        data = request.POST
        data_ = dict(data)

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question= course_exam_question.objects.get(text=k)
            questions.append(question)
        user=request.user
        quiz= course_exam.objects.get(pk=1)

        score = 0
        multiplier= 100 / len(quiz.get_questions())
        results = []
        correct_answer= None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = course_exam_answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer=a.text
                
                results.append({str(q):{'correct_answer': correct_answer,'answered': a_selected}})
            else:
                results.append({str(q):'not answered'})
        score_ = score * multiplier 
        course_exam_result.objects.create(exam=quiz, user=user, score=score_)
        
        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed':True, 'score':score_, 'results':results})
        else:
            return JsonResponse({'passed':False, 'score':score_, 'results':results})
    
def course_test(request,coursePk):
    course=onlineCourseList.objects.get(pk=coursePk)
    videos=allCourseVideos.objects.filter(name=course)
    exam=course_exam.objects.get(pk=1)
    questions=[]
    for q in exam.get_questions():
        answers=[]
        for ans in q.get_answers():
            answers.append(ans.text)
        questions.append({str(q):answers})
    # print(questions)
    return render(request,'course-test.html',{'videos':videos,'exam':exam,'time':exam.time,'noOfQuestion':len(questions),'course':course,'questions':questions})

def course_test_exam(request,coursePk,examPk):
    course=onlineCourseList.objects.get(pk=coursePk)
    exam=course_exam.objects.get(pk=examPk)
    questions=[]
    for q in exam.get_questions():
        answers=[]
        for ans in q.get_answers():
            answers.append(ans.text)
        questions.append({str(q):answers})
    return render(request,'course-test-exam.html',{'exam':exam,'time':exam.time,'noOfQuestion':len(questions),'course':course,'questions':questions})
    
def course_user_request(request,pk):
    if request.method=='POST':
        transection_id = request.POST['transection_id_template']
        course=onlineCourseList.objects.get(id=pk)
        course_stu= onlineCourseStudents(course=course, student=request.user,transection_id=transection_id, status=False)
        course_stu.save()
    active=onlineCourseStudents.objects.filter(course=course,student=request.user,status=True).exists()
    pending=onlineCourseStudents.objects.filter(course=course,student=request.user).exists()
    if active:
        active=1
    else: active=0
    if pending:
        pending=1
    else: pending=0
    request.session['active']= active
    request.session['pending']= pending
    return redirect("courseOutlineOnline", pk=pk)
def live_course_user_request(request,coursePk):
    if request.method=='POST':
        transection_id = request.POST['transection_id_template']
        course=liveCourseList.objects.get(id=coursePk)
        course_stu= liveCourseStudents(course=course, student=request.user,transection_id=transection_id, status=False)
        course_stu.save()
    active=liveCourseStudents.objects.filter(course=course,student=request.user,status=True).exists()
    pending=liveCourseStudents.objects.filter(course=course,student=request.user).exists()
    if active:
        active=1
    else: active=0
    if pending:
        pending=1
    else: pending=0
    request.session['active']= active
    request.session['pending']= pending
    return redirect("courseOutlineLive", coursePk=coursePk)
def live_course(request):
    return render(request,'live-courses.html')

def questions(request):
    all=allquestion.objects.filter(approved=True).order_by('-timestamp')
    users_qus=NULL
    if request.user.is_authenticated:
        
        users_qus=allquestion.objects.filter(auther=request.user)
    return render(request,'questions.html',{'all':all,'users_qus':users_qus})

def singleQuestion(request,qusPk):
    qus=allquestion.objects.get(pk=qusPk)
    answers=qus.get_all_answers()
    write_answer_form=add_answers()
    return render(request,'single-question.html',{'qus':qus,'answers':answers,'write_answer_form':write_answer_form})
def write_an_answer(request,qusPk):
    form=add_answers(use_required_attribute=False)
    qus=allquestion.objects.get(pk=qusPk)
    if request.method=='POST':
        form=add_answers(request.POST)
        if form.is_valid():
            obj=question_answer()
            obj.answer=form.cleaned_data['answer']
            obj.auther=request.user
            obj.question=qus
            obj.save()
    return redirect("single-question",qusPk=qusPk)
def courseOutlineOnline(request,pk):
    if request.user.is_authenticated:
        course=onlineCourseList.objects.get(id=pk)
        active=onlineCourseStudents.objects.filter(course=course,student=request.user,status=True).exists()
        pending=onlineCourseStudents.objects.filter(course=course,student=request.user).exists()
        if active:
            active=1
        else: active=0
        if pending:
            pending=1
        else: pending=0
        return render(request,'course-outline.html',{'id':pk,'active':active,'pending':pending})
    return render(request,'course-outline.html')
def courseOutlineLive(request,coursePk):
    if request.user.is_authenticated:
        course=liveCourseList.objects.get(id=coursePk)
        active=liveCourseStudents.objects.filter(course=course,student=request.user,status=True).exists()
        pending=liveCourseStudents.objects.filter(course=course,student=request.user).exists()
        if active:
            active=1
        else: active=0
        if pending:
            pending=1
        else: pending=0
        return render(request,'live-course-outline.html',{'course':course,'active':active,'pending':pending})
    return render(request,'live-course-outline.html')
def bookmark(request):
    if request.method=='POST':
        id=request.POST.get('sid')
        id=int(id)
        post=allBlogs.objects.get(id=id)
        bookmark=allBlogs.objects.filter(id=id,bookmark=request.user).exists()
        if bookmark:
            post.bookmark.remove(request.user)
        else:
            post.bookmark.add(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
def ask_question(request):
    form=add_question(use_required_attribute=False)
    if request.method=='POST':
        form=add_question(request.POST)
        if form.is_valid():
            obj=allquestion()
            obj.title=form.cleaned_data['title']
            obj.auther=request.user
            obj.question=form.cleaned_data['question']
            obj.save()
    return render(request,'ask-question.html',{'form':form})
def the_course(request,coursePk,pk):
    course=onlineCourseList.objects.get(pk=coursePk)
    video=allCourseVideos.objects.get(pk=pk)
    allvid=allCourseVideos.objects.filter(name=video.name)
    return render(request,'course-contents.html',{'video':video,'all':allvid,'course':course})

def course_about(request):
    course=onlineCourseList.objects.get(pk=10)
    videos=allCourseVideos.objects.filter(name=course)
    return render(request,'course-about.html',{'videos':videos,'course':course})

def dislike(request):
    if request.method=='POST':
        id=request.POST.get('siddis')
        id=int(id)
        post=allBlogs.objects.get(id=id)
        is_liked=allBlogs.objects.filter(id=id,likes=request.user).exists()
        is_disliked=allBlogs.objects.filter(id=id,dislikes=request.user).exists()
        if is_liked:
            post.likes.remove(request.user)
        if is_disliked :
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
def like(request):
    if request.method=="POST":
        id=request.POST.get('sid')
        id=int(id)
        post=allBlogs.objects.get(id=id)
        is_liked=allBlogs.objects.filter(id=id,likes=request.user).exists()
        is_disliked=allBlogs.objects.filter(id=id,dislikes=request.user).exists()
        if is_disliked:
            post.dislikes.remove(request.user)
        if is_liked :
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
def bookmarked_blogs(request):
    liked_blogs=allBlogs.objects.filter(likes=request.user)
    disliked=allBlogs.objects.filter(dislikes=request.user)
    blogs=allBlogs.objects.filter(bookmark=request.user)
    return render(request,'bookmarked-blogs.html',{'liked':liked_blogs,'disliked':disliked,'blogs':blogs})
def blogs(request):
    blogs=allBlogs.objects.all()
    liked_blogs=allBlogs.objects.filter(likes=request.user)
    disliked=allBlogs.objects.filter(dislikes=request.user)
    bookmark=allBlogs.objects.filter(bookmark=request.user)
    return render(request,'blogNew.html',{'blogs':blogs,'liked':liked_blogs,'disliked':disliked,'bookmark':bookmark})
def searchBlogs(request):
    if request.method == 'POST':
        searched=request.POST
        print(searched)
        blogs=allBlogs.objects.filter(title__contains=searched)
        return JsonResponse({'searchedBlogs':blogs})
def blogSingle(request,blogPk):
    blog=allBlogs.objects.get(pk=blogPk)
    return render(request,'blog-single.html',{'blog':blog})

def write_a_blog(request):
    form=add_blog(use_required_attribute=False)
    if request.method=='POST':
        form=add_blog(request.POST)
        if form.is_valid():
            obj=allBlogs()
            obj.title=form.cleaned_data['title']
            obj.auther=request.user
            obj.the_blog=form.cleaned_data['blog']
            obj.save()
    return render(request,'writeBlogs.html',{'form':form})
def my_blogs(request):
    blogs=allBlogs.objects.filter(auther=request.user)
    liked_blogs=allBlogs.objects.filter(likes=request.user)
    disliked=allBlogs.objects.filter(dislikes=request.user)
    bookmark=allBlogs.objects.filter(bookmark=request.user)
    return render(request,'my-blogs.html',{'blogs':blogs,'liked':liked_blogs,'disliked':disliked,'bookmark':bookmark})
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
    return redirect("articles", pk=post.pk)
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