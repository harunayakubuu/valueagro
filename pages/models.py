from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()


class AboutUs(models.Model):
    about = RichTextField()
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.created_date)


class PrivacyPolicy(models.Model):
    # title = models.CharField(max_length = 255)
    policy = RichTextField()
    active = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.created_date)
    
    class Meta:
        verbose_name_plural = "Privacy Policy"


class TermsAndCondition(models.Model):
    # term = models.CharField(max_length = 255)
    terms_and_conditions = RichTextField()
    active = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.created_date)


class Service(models.Model):
    title = models.CharField(max_length = 255, unique = True)
    description = RichTextField()
    picture = models.ImageField(upload_to = "pictures/services")
    active = models.BooleanField("Active", default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title


class Testimonials(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    testimony = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)

    public = models.BooleanField(default = False)

    def __str__(self):
        return self.user.get_full_name