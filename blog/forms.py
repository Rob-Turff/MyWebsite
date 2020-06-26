from django import forms

from .models import Post, UniYear, Skills, Job, CvProject, AdditionalInfo


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


class CvProjectForm(forms.ModelForm):
    class Meta:
        model = CvProject
        fields = ('title', 'date', 'description',)


class AdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = AdditionalInfo
        fields = ('text',)


class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}), required=True)
