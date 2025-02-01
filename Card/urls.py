from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('generate_invite/', views.generate_inviteCode_view, name='generate_invite'),
    path('food/', views.food_view, name='food'),
    path('<slug:user>/modules/', views.user_library_view, name='user_library'),
    path('module/add/', views.modul_view, name='module_add'),
    path('module/<slug:module_slug>', views.modul_view, name='module'),
    path("delete-flashcard/", views.delete_flashcard_view, name="delete_flashcard"),

]

