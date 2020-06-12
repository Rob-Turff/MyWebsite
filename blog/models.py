from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.TextField()
    image = models.ImageField(upload_to='images/projects/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class UniYear(models.Model):
    year = models.CharField(max_length=100)
    grades = models.TextField()
    overall_grade = models.TextField()

    def __str__(self):
        return self.year


class Skills(models.Model):
    first_col = models.TextField()
    second_col = models.TextField()

    def __str__(self):
        return 'Skills section'


class Job(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class CvProject(models.Model):
    title = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class AdditionalInfo(models.Model):
    text = models.TextField()

    def __str__(self):
        return 'Additional Info Section'
