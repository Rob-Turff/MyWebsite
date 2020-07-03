from django.db import models


class Management(models.Model):
    ip = models.CharField(max_length=15)

    def __str__(self):
        return 'Management Data'
