from django.db import models


class Task(models.Model):

    def __str__(self):
        return self.title

    parsed_url = models.URLField()
    title = models.CharField(max_length=127)
    description = models.CharField(max_length=1023)
    site_name = models.CharField(max_length=127)
    image_url = models.URLField()
    date = models.DateTimeField(auto_now_add=True)
