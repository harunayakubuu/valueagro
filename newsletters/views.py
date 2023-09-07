from django.shortcuts import render, redirect
from . models import Subscriber, MailMessage
from . forms import SubscriptionForm, SubscriptionEditForm, MailMessageCreateForm, MailMessageEditForm
from django.conf import settings
from django.contrib import messages

from django.core.mail import send_mail
from django_pandas.io import read_frame


def subscription_form(request):
    form = SubscriptionForm()
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscription successful.")

            return redirect('newsletters:subscription_form')
        else:
            messages.error(request, "Invalid input")
    context = {
        'form': form
    }
    return render(request, "newsletters/subscription_form.html", context)


def email_list(request):
    email_list = Subscriber.objects.all()
    context = {
        'email_list': email_list
    }
    return render(request, "newsletters/email_list.html", context)


def mail_message_form(request):
    emails = Subscriber.objects.filter(subscribed = True)
    df = read_frame(emails, fieldnames = ['email'])
    mail_list = df['email'].values.tolist()
    
    form = MailMessageCreateForm()
    if request.method == "POST":
        form = MailMessageCreateForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit = False)
            
            subject = form_instance.title
            message = form_instance.message

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                mail_list,
                fail_silently = False
            )

            messages.success(request, "Email sent.")
            return redirect('newsletters:mail_message_form')
        else:
            messages.error(request, "Invalid form")
    context = {
        'form': form
    }
    return render(request, "newsletters/mail_message_form.html", context)


def mail_messages_list(request):
    messages_list = MailMessage.objects.all()
    context = {
        'messages_list': messages_list
    }
    return render(request, "newsletters/mail_messages_list.html", context)