from django import forms

from .models import Post, UniYear


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class EduForm(forms.ModelForm):

    class Meta:
        model = UniYear
        fields = ('year', 'grades', 'overall_grade',)
