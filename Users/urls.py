from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.signupView, name='signup'),
    path('login', views.loginView, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('users_library/', views.users_library, name='users_library'),
    path('generate_invite/', views.generate_inviteCode_view, name='generate_invite'),
]