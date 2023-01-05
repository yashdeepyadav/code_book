from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm,ProfileForm
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from datetime import datetime
import logging
import sys

logger=logging.getLogger()


# Create your views here.

def registerUser(request):

    if request.user.is_authenticated:
        return redirect('profiles')

    form=CustomUserCreationForm()

    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,"New user created")
            login(request,user)
            return redirect('editAccount')

        else:

            messages.error(request,"ERROR")



    context={"page":"register","form":form}
    return render(request,'users/login_register.html',context)


def loginUser(request):
    
    context={"page":"login"}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method=='POST':
        uname=request.POST['username']
        passw=request.POST['password']
        
        try:
            user=User.objects.get(username=uname)
        except:
            messages.error(request,'Username not found')
            print("Username not FOUND!!!")

        user=authenticate(request,username=uname,password=passw)

        if user is not None:
            login(request,user)
            messages.success(request,'Logged in successfully')
            return redirect('profiles')

        else:
            messages.warning(request,'Username or Password incorrect')
        

    return render(request,'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.success(request,'Loggedout Successfully')
    return redirect('login')



def profiles(request):

    profiles=Profile.objects.all()

    context={'profiles':profiles}


    return render(request,'users/profiles.html',context)

def profile(request,id):

    profile=Profile.objects.get(id=id)

    skills_desc=profile.skill_set.exclude(description__exact="")
    skills_empty=profile.skill_set.filter(description="")

    context={'profile':profile,"skills_desc":skills_desc,"skills_empty":skills_empty}
    
    return render(request,'users/profile.html',context)

@login_required(login_url="login")
def userAccount(request):
    profile=request.user.profile
    skills=profile.skill_set.all()
    projects=profile.project_set.all()

    context={'profile':profile,'skills':skills,'projects':projects}

    return render(request,'users/account.html',context)

@login_required(login_url="login")
def editAccount(request):
    profile=request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)

        if form.is_valid:
            form.save()
            return redirect('account')


    context={"form":form}

    return render(request,'users/editAccount.html',context)

