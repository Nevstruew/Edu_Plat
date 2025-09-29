from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Assignment
from .forms import LessonForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

def lesson_list(request):
    lessons = Lesson.objects.select_related('course', 'created_by').all()
    return render(request, 'lessons/list.html', {'lessons': lessons})

def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    assignments = lesson.assignments.all()
    return render(request, 'lessons/detail.html', {
        'lesson': lesson,
        'assignments': assignments
    })

@login_required
def lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.created_by = request.user
            lesson.save()
            return redirect('lesson_detail', pk=lesson.pk)
    else:
        form = LessonForm()
    return render(request, 'lessons/create.html', {'form': form})

@login_required
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_detail', pk=lesson.pk)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'lessons/edit.html', {'form': form})