from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('register/', views.register, name='register'),
]