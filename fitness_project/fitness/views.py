from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, SkillForm
from django.contrib import messages


def home(request):
    return render(request, 'fitness/home.html')


def profiles(request):
    prof = Profile.objects.all()
    context = {'profiles': prof}
    return render(request, 'fitness/profiles.html', context)


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'fitness/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:

                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()

                login(request, user)
                return redirect('account')
            except IntegrityError:
                return render(request, 'fitness/signupuser.html',
                              {'form': UserCreationForm(), 'error':
                                  'Такое имя пользователя уже существует. Задайте другое!'})
        else:
            return render(request, 'fitness/signupuser.html',
                          {'form': UserCreationForm(), 'error':
                              'Пароли не совпадают!!!'})


def coach(request, pk):
    prof = Profile.objects.get(id=pk)

    context = {
        'profile': prof,
    }
    return render(request, 'fitness/coach.html', context)


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'fitness/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'fitness/loginuser.html', {
                'form': AuthenticationForm(),
                'error': 'Неверные данные для входа!!!'})
        else:
            login(request, user)
            return redirect('account')


@login_required(login_url='loginuser')
def user_account(request):
    prof = request.user.profile
    skills = prof.skill_set.all()

    context = {
        'profile': prof,
        'skills': skills,
    }
    return render(request, 'fitness/account.html', context)


@login_required(login_url='loginuser')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'fitness/profile_form.html', context)


@login_required(login_url='loginuser')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('account')

    context = {"form": form}
    return render(request, 'fitness/skill_form.html', context)


@login_required(login_url='loginuser')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect('account')

    context = {'form': form}
    return render(request, 'fitness/skill_form.html', context)


@login_required(login_url='loginuser')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect('account')

    context = {'object': skill}
    return render(request, 'fitness/delete.html', context)


