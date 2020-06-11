from django import forms

from .models import Post, UniYear, Skills, Job, Project


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class EduForm(forms.ModelForm):
    class Meta:
        model = UniYear
        fields = ('year', 'grades', 'overall_grade',)


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ('first_col', 'second_col',)


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'location', 'date', 'description',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'title', 'date', 'description', 'cv_description', 'display_on_cv', 'display_on_portfolio', 'link', 'image')
