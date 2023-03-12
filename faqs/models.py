from django.db import models
from django.utils.text import slugify
# from ckeditor.fields import RichTextField


class Faq(models.Model):
    question    = models.CharField(max_length = 255)
    slug        = models.SlugField(max_length=255)
    answer      = models.TextField()
    active      = models.BooleanField('Active', default = False)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.question

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
        return super(Faq, self).save(*args, **kwargs)