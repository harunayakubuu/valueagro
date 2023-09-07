from django.db import models
from ckeditor.fields import RichTextField


class Subscriber(models.Model):

    email = models.EmailField(unique = True)
    subscribed = models.BooleanField(default = True)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.email


class MailMessage(models.Model):

    title = models.CharField(max_length = 200, unique = True)
    message = RichTextField()
    active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.email