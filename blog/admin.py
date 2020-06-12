from django.contrib import admin
from .models import Post, Project, UniYear, Skills, Job, CvProject, AdditionalInfo

admin.site.register(Post)
admin.site.register(Project)
admin.site.register(UniYear)
admin.site.register(Skills)
admin.site.register(Job)
admin.site.register(CvProject)
admin.site.register(AdditionalInfo)