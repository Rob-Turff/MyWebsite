from django.db import models


class StaticIp(models.Model):
    title = models.CharField(primary_key=True, max_length=30)
    ip = models.CharField(max_length=15)

    def __str__(self):
        return self.title + ":" + self.ip
