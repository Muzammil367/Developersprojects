from email import message
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles,
    }
    return render(request, 'all-profiles.html', context)

def profile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkill = profile.skill_set.exclude(description='')

    otherSkill = profile.skill_set.filter(description='')

    context = {'profile': profile,
                'topSkill': topSkill, 'otherSkill': otherSkill}
    return render(request, 'single-profile.html', context)

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('projects:project-all')

    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "User successfully logged in")
            return redirect('projects:project-all')
        else:
            messages.error(request, "Username or password doesn't match")

    context = {'page': page}
    return render(request, 'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.success(request, 'User logged out')
    return redirect('users:login')


def registerUser(request):
    page = 'register'

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User created successfully')
            return redirect('users:login')
        else:
            messages.error(request, 'some error occurred')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

@login_required(login_url='users:login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated Successfully')
            return redirect('users:account')

    context = {'form': form}
    return render(request, 'users/edit_account.html', context)

@login_required(login_url='users:login')
def userAccount(request):
    profile = request.user.profile

    context = {'profile': profile}
    return render(request, 'users/account.html', context)

def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill created Successfully')
            return redirect('users:account')
        else:
            messages.error(request, 'Some error occurred')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)

@login_required(login_url='users:login')
def deleteSkill(request,pk):
    profile

