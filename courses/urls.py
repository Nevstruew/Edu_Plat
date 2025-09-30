from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('register/', views.register, name='register'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    path('assignment/<int:assignment_id>/submissions/', views.assignment_submissions, name='assignment_submissions'),
]
