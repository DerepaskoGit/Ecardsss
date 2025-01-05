from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm

def index(request):
    return redirect('login')

def signupView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
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
            print('yesyesnono')
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('users_library')
    else:
        form = LoginForm()

    Data = {
        'form':form
    }

    return render(request, 'Users/login.html', Data)


def users_library(request):
    Data = {

    }

    return render(request, 'Users/users_library.html', Data)