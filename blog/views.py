from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from mysite.settings import EMAIL_HOST_USER
from .forms import PostForm, EduForm, SkillsForm, JobForm, CvProjectForm, AdditionalInfoForm, ContactForm
from .models import Post, Project, UniYear, Skills, Job, CvProject, AdditionalInfo
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'mainpage/home.html', {})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def project_detail(request, pk):
    projects = Project.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    displayed_project = get_object_or_404(Project, pk=pk)
    return render(request, 'portfolio/project_list.html',
                  {'projects': projects, 'displayed_project': displayed_project})


def project_list(request):
    projects = Project.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    displayed_project = projects.first()
    return render(request, 'portfolio/project_list.html',
                  {'projects': projects, 'displayed_project': displayed_project})


def cv_home(request):
    years = UniYear.objects.all()
    skills = Skills.objects.first()
    jobs = Job.objects.all()
    projects = CvProject.objects.all()
    additional_info = AdditionalInfo.objects.first()
    return render(request, 'cv/cv_home.html', {'years': years, 'skills': skills, 'jobs': jobs, 'projects': projects,
                                               'additional_info': additional_info})


@login_required
def cv_edu_new(request):
    if request.method == "POST":
        form = EduForm(request.POST)
        if form.is_valid():
            uni_year = form.save(commit=False)
            uni_year.save()
            return redirect('cv_home')
    else:
        form = EduForm()
    return render(request, 'cv/edu_edit.html', {'form': form})


@login_required
def cv_edu_edit(request, pk):
    uni_year = get_object_or_404(UniYear, pk=pk)
    if request.method == "POST":
        form = EduForm(request.POST, instance=uni_year)
        if form.is_valid():
            uni_year = form.save(commit=False)
            uni_year.save()
            return redirect('cv_home')
    else:
        form = EduForm(instance=uni_year)
    return render(request, 'cv/edu_edit.html', {'form': form})


@login_required
def cv_skills_edit(request):
    if request.method == "POST":
        if Skills.objects.count() == 1:
            skill_obj = Skills.objects.first()
            form = SkillsForm(request.POST, instance=skill_obj)
        else:
            form = SkillsForm(request.POST)
        if form.is_valid():
            skill_obj = form.save(commit=False)
            skill_obj.save()
            return redirect('cv_home')
    else:
        if Skills.objects.count() == 1:
            skill_obj = Skills.objects.first()
            form = SkillsForm(instance=skill_obj)
        else:
            form = SkillsForm()
    return render(request, 'cv/skills_edit.html', {'form': form})


@login_required
def cv_job_new(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            return redirect('cv_home')
    else:
        form = JobForm()
    return render(request, 'cv/job_edit.html', {'form': form})


@login_required
def cv_job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            return redirect('cv_home')
    else:
        form = JobForm(instance=job)
    return render(request, 'cv/job_edit.html', {'form': form})


@login_required
def cv_project_new(request):
    if request.method == "POST":
        form = CvProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('cv_home')
    else:
        form = CvProjectForm()
    return render(request, 'cv/templates/portfolio/cv_project_edit.html', {'form': form})


@login_required
def cv_project_edit(request, pk):
    project = get_object_or_404(CvProject, pk=pk)
    if request.method == "POST":
        form = CvProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('cv_home')
    else:
        form = CvProjectForm(instance=project)
    return render(request, 'cv/templates/portfolio/cv_project_edit.html', {'form': form})


@login_required
def cv_additional_info_edit(request):
    if request.method == "POST":
        if AdditionalInfo.objects.count() == 1:
            additional_info_obj = AdditionalInfo.objects.first()
            form = AdditionalInfoForm(request.POST, instance=additional_info_obj)
        else:
            form = AdditionalInfoForm(request.POST)
        if form.is_valid():
            additional_info_obj = form.save(commit=False)
            additional_info_obj.save()
            return redirect('cv_home')
    else:
        if AdditionalInfo.objects.count() == 1:
            additional_info_obj = AdditionalInfo.objects.first()
            form = AdditionalInfoForm(instance=additional_info_obj)
        else:
            form = AdditionalInfoForm()
    return render(request, 'cv/additional_info_edit.html', {'form': form})


def contact_page(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                EmailMessage(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER], headers={'Reply-To': email}).send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('home')
    return render(request, "mainpage/contact.html", {'form': form})
