from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from .models import InviteCodeDb

class UserLibraryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'maxlength':'4', 'name': 'emaiwwwl'}))

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введите логин или email",
            'id': 'email',
            'name': 'email',
    }))

    password = forms.CharField(
        max_length=25, 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Введите пароль",
            'id': 'pwd',
            'name': 'password'
        }))
    

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

        



class RegisterForm(forms.ModelForm):  
    email = forms.EmailField( 
        min_length=6,
        max_length=40,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "Введите email",
            'id': 'email',
    }))

    username = forms.CharField( 
        min_length=4,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введите имя пользователя",
            'id': 'username',
            'maxlength':'8',
    }))

    password = forms.CharField(
        min_length=4,
        max_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Введите пароль",
            'id': 'password',
            'maxlength':'8', 
    }))

    repeat_password = forms.CharField(
        min_length=4,
        max_length=8,
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Повторите пароль",
        'id': 'repassword',
        'name': 'repeat_password',
    }))

    invite_code = forms.CharField( 
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введите invite code",
            'id': 'invite_code',
            'name': 'invite_code',
    }))


    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('Логин занят')
        return username

    def clean(self):
        cd = self.cleaned_data
        password = cd.get('password')
        repeat_password = cd.get('repeat_password')

        if password and repeat_password and password != repeat_password:
            self.add_error('repeat_password', 'Пароли не совпадают')
        return cd
    
    def clean_invite_code(self):
        invite_code = self.cleaned_data['invite_code']
        if InviteCodeDb.objects.filter(invite_code=invite_code).exists():
           return invite_code
        raise forms.ValidationError('Неверный invite code')
    
    