from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup_view, name='signup'),
    path('check_username/', views.check_username, name='check_username'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_user, name='logout'),
]
