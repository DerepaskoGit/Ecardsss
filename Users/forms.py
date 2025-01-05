from django import forms

class RegisterForm(forms.Form):  
    email = forms.EmailField(
        max_length=25,
        widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': "Введите email",
        'id': 'email',
        'name': 'email'
    }))

    username = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Введите имя пользователя",
        'id': 'username',
        'name': 'username'
    }))

    password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Введите пароль",
        'id': 'pwd',
        'name': 'password'
    }))

    repeat_password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Введите пароль",
        'id': 'repwd',
        'name': 'repassword'
    }))

    # invite_code = forms.CharField(
    #     max_length=25,
    #     widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': "Invite-сode",
    #     'id': 'Invite',
    #     'name': 'Invite-code'
    # }))

    # class Meta:
    #     model = get_user_model()
