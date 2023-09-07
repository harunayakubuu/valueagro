from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.contrib import messages


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.SlugField(max_length = 50, unique = True)
    active = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Activity(models.Model):
    author      = models.ForeignKey(User, on_delete = models.CASCADE)
    title       = models.CharField(max_length = 128, unique = True)
    category    = models.ForeignKey(Category, on_delete = models.CASCADE)
    
    image       = models.ImageField(upload_to = 'pictures/activities/', help_text = "Width:800 X Height:562")
    content     = models.TextField()
    active      = models.BooleanField("Active", default = False)
    slug        = models.SlugField(max_length = 150, unique = True)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:public-activity-details', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Activity, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Activities'