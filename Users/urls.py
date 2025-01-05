from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signup/', views.signupView, name='signup'),
    path('login/', views.loginView, name='login'),
    path('users_library', views.users_library, name='users_library')
]