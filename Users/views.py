from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, UserLibraryForm


def signup_view(request):
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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, 'Логин или пароль не совпадают')
    else:
        form = LoginForm()

    Data = {
        'form':form
    }

    return render(request, 'Users/login.html', Data)


def check_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    return JsonResponse(response)


def logout_user(request):
    logout(request)
    return redirect('login')