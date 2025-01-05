from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm

def index(request):
    return redirect('signup')

def signup(request):
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


def login(request):
    Data = {

    }

    return render(request, 'Users/login.html', Data)