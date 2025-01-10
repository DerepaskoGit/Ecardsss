from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('users_library/', views.users_library, name='users_library'),
    path('generate_invite/', views.generate_inviteCode_view, name='generate_invite'),
]