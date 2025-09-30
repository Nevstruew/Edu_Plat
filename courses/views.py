from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Course, Lesson, Assignment, Submission
from .forms import LessonForm, SubmissionForm

# Проверка является ли пользователь преподавателем
def is_teacher(user):
    return user.is_staff or user.is_superuser

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

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all().order_by('title')
    return render(request, 'courses/detail.html', {
        'course': course,
        'lessons': lessons
    })

def lesson_list(request):
    try:
        lessons = Lesson.objects.select_related('course', 'created_by').all().order_by('course__title', 'title')
    except Exception as e:
        lessons = Lesson.objects.all().order_by('course__title', 'title')
    
    return render(request, 'lessons/list.html', {'lessons': lessons})

def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    assignments = lesson.assignments.all()
    return render(request, 'lessons/detail.html', {
        'lesson': lesson,
        'assignments': assignments
    })

@login_required
@user_passes_test(is_teacher)
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
@user_passes_test(is_teacher)
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

def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    submissions = assignment.submissions.filter(student=request.user) if request.user.is_authenticated else []
    
    can_submit = request.user.is_authenticated and not submissions.exists()
    
    return render(request, 'assignments/assignment_detail.html', {
        'assignment': assignment,
        'user_submission': submissions.first(), 
        'can_submit': can_submit 
    })

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    existing_submission = Submission.objects.filter(
        assignment=assignment, 
        student=request.user
    ).first()
    
    if existing_submission:
        messages.warning(request, 'Вы уже отправили ответ на это задание.')
        return redirect('assignment_detail', assignment_id=assignment_id)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            
            messages.success(request, 'Ваш ответ успешно отправлен!')
            return redirect('assignment_detail', assignment_id=assignment_id)
    else:
        form = SubmissionForm()
    
    return render(request, 'assignments/submit_assignment.html', {
        'form': form,
        'assignment': assignment
    })

@login_required
def submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    is_teacher = request.user == submission.assignment.lesson.created_by
    is_owner = request.user == submission.student
    
    if not (is_teacher or is_owner):
        messages.error(request, 'У вас нет прав для просмотра этого ответа.')
        return redirect('home')
    
    if is_teacher and request.method == 'POST':
        grade = request.POST.get('grade')
        feedback = request.POST.get('feedback', '')
        
        if grade:
            submission.grade = int(grade)
            submission.feedback = feedback
            submission.save()
            messages.success(request, 'Оценка сохранена!')
            return redirect('assignment_submissions', assignment_id=submission.assignment.id)
        else:
            messages.error(request, 'Пожалуйста, укажите оценку.')
    
    return render(request, 'assignments/submission_detail.html', {
        'submission': submission
    })

@login_required
def assignment_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if request.user != assignment.lesson.created_by:
        messages.error(request, 'У вас нет прав для просмотра ответов на это задание.')
        return redirect('home')
    
    submissions = assignment.submissions.all().order_by('-submitted_at')
    
    return render(request, 'assignments/assignment_submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })
    