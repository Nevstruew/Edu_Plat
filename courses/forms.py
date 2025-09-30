from django import forms
from .models import Lesson, Submission

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={
                'rows': 10, 
                'placeholder': 'Введите ваш ответ на задание...',
                'class': 'form-control'
            })
        }
