from django.db import models
from ckeditor.fields import RichTextField


class Partner(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    logo = models.ImageField(upload_to = 'pictures/partners', help_text = "Width:160px X Height:100px")
    about = RichTextField(blank=True, null=True)
    # country = models.CharField(max_length=60, blank=True, null=True)
    
    website = models.URLField(blank = True, null = True)
    active = models.BooleanField(default = True)
    slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'