from django import forms
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }