from email import message
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill
from .forms import CustomerUserCreationForm,ProfileForm,SkillForm
from django.contrib.auth.decorators import login_required
from .utils import paginateProfiles, searchProfiles

from django.db.models import Q
# Create your views here.

def loginUser(request):
    page="register"


    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            #print('Username does not exist')
            messages.error(request,'Username does not exist')

        user = authenticate(request,username=username,password=password) # match

        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,'Username or Password is incorrect!')
            print('Username or Password is incorrect!')


    
    return render(request,'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request,'User was logged out!')
    return redirect('login')


def profiles(request):
    profiles,search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request,profiles,3)
    
    context = {'profiles':profiles,'search_query':search_query,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)

def registerUser(request):
    page="register"
    form = CustomerUserCreationForm()
    if request.method == "POST":
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"User account was created")

            login(request,user)
            return redirect('edit-account')

        else:
            messages.error(request,"Error has occured during registeration")

    context = {"page":page,'form':form}
    return render(request,'users/login_register.html',context)



def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile':profile, 'topSkills': topSkills, 'otherSkills':otherSkills}

    return render(request,'users/user-profile.html',context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()


    context = {'profile':profile, 'skills': skills, "projects":projects}
    return render(request,'users/account.html',context)


@login_required(login_url="login")
def editAccount(request):
    profile=request.user.profile
    
    form=ProfileForm(instance=profile)
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context={"form":form}
    return render(request, 'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form=SkillForm()
    if request.method=="POST":
        form=SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'Successfully added a new skill!')
            return redirect('account')
    context={'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)

    if request.method=="POST":
        form=SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully updated a new skill!')
            return redirect('account')
    context={'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url="login")
def deleteSkill(request,pk):
    profile = request.user.profile
    skill=profile.skill_set.get(id=pk)
    if request.method=="POST":
        skill.delete()
        messages.success(request,'Successfully deleted a new skill!')
        return redirect("account")
    context = {'object': skill}
    return render(request,"delete_template.html",context)
