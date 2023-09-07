from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


class Contact(models.Model):
    name  = models.CharField(max_length = 50, verbose_name='Name')
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = PhoneNumberField(verbose_name="Phone number")
    SUBJECT_CHOICES = (
        ('complaint', 'Complaint'),
        ('customer care', 'Customer Care'),
        ('Enquiries', 'Enquiries'),
        ('sales', 'Sales'),
    )
    subject     = models.CharField(max_length = 20, choices = SUBJECT_CHOICES)
    STATUS_CHOICES = (
        ('attended', 'Attended'),
        ('ignored', 'Ignored'),
        ('pending', 'Pending'),
    )
    message     = models.TextField()
    status      = models.CharField(max_length = 20, choices = STATUS_CHOICES, default="pending")
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    def get_message_details(self):
        return reverse('contacts:contact-message-details', args=[self.id])