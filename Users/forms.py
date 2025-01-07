from django import forms
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введите логин или email",
            'id': 'email',
            'name': 'email'
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
    repeat_password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Повторите пароль",
        'id': 'repwd',
        'name': 'repeat_password'
    }))

    

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']
        
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите email"
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите имя пользователя"
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите пароль"
            })
        }

    def clean(self):
        cd = self.cleaned_data
        password = cd.get('password')
        repeat_password = cd.get('repeat_password')

        if password and repeat_password and password != repeat_password:
            self.add_error('repeat_password', 'Пароли не совпадают')
        
        return cd
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует')
        return email
 


