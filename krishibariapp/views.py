from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import  redirect, render
from .models import Dbtable
from django.contrib import messages
from .models import videoTable
# Create your views here.

def homepage(request):
    # if request.method=='POST':
    #     if request.POST.get('login'):
    #         return render(request,'login.html')
    #     if request.POST.get('register'):
    #         return render(request,'register.html')
    # if request.user.is_authenticated:
    #         return render(request,'home.html',{'Login':})
    video=videoTable.objects.all()
    return render(request,'home.html',{"video":video})
def log_out(request):
    logout(request)
    return redirect('/')
def profile(request):
    return render(request,'userProfile.html')
def insertrecord(request):
    if request.method=='POST':
        # if request.POST.get('name') and request.POST.get('email') and request.POST.get('password'):
        #      saverecord=Dbtable()
        #      saverecord.name=request.POST.get('name')
        #      saverecord.email=request.POST.get('email')
        #      saverecord.password=request.POST.get('password')
        #      saverecord.save()
        # 
        name=request.POST['name']
        # username=request.POST['username']
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
    # return render(request,'login.html')
    
    if request.method == 'POST':
        name = request.POST['name']
        email =request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email,name=name, password=password)
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
def add(request):
    # val1=int(request.GET['num1'])
    # val2=int(request.GET['num2'])
    # res=val1+val2
    return render(request,'login.html')