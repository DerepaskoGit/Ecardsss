from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import InviteCodeDb
from .forms import RegisterForm, LoginForm
from .utils import generate_inviteCode

def index(request):
    return redirect('login')

def signupView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            return render(request, 'Users/register_done.html')
    else:
        form = RegisterForm()
        
    
    Data = {
        'form': form
    }

    return render(request, 'Users/signup.html', Data)


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('users_library')
            else:
                form.add_error(None, 'Логин или пароль не совпадают')
    else:
        form = LoginForm()

    Data = {
        'form':form
    }

    return render(request, 'Users/login.html', Data)


def generate_inviteCode_view(request):
    if request.method == 'POST':
        invite = generate_inviteCode(request.user)
        return JsonResponse({'invite_code':invite.invite_code})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def users_library(request):
    Data = {
        
    }

    return render(request, 'Users/users_library.html', Data)


def logout_user(request):
    logout(request)
    return redirect('login')