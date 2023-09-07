from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TermsAndCondition, PrivacyPolicy, Service, Testimonial
from .forms import (
    PrivacyPolicyForm, PrivacyPolicyEditForm,
    TermsAndConditionForm, TermsAndConditionEditForm,
    ServiceForm, ServiceEditForm, TestimonialForm#, AboutUsForm
)
from django.contrib import messages
from blog.models import Activity
from partners.models import Partner
from accounts.models import Team
from blog.models import Activity
from faqs.models import Faq
from products.models import Product

from django.contrib.auth import get_user_model
User = get_user_model()


def index(request):
    services = Service.objects.order_by("-created_date").filter(active = True)
    partners = Partner.objects.order_by("-created_date").filter(active = True)
    recent_activities = Activity.objects.order_by("-created_at").filter(active = True)[:6]
    team = Team.objects.filter(active = True)
    answered_questions = Faq.objects.all()
    products = Product.objects.order_by("-created_at").filter(available = True, public=True)[:6]
    
    context = {
        'recent_activities': recent_activities,
        'services': services,
        'team': team,
        'answered_questions': answered_questions,
        'products': products
    }
    return render(request, 'pages/index.html', context)
    

def about_us(request):
    services = Service.objects.order_by("-created_date").filter(active = True)
    partners = Partner.objects.order_by("-created_date").filter(active = True)
    team = Team.objects.filter(active = True)
    testimonials = Testimonial.objects.filter(approved = True, public = True)
    answered_questions = Faq.objects.filter(active = True)

    context = {
        'partners': partners,
        'services': services,
        'team': team,
        'answered_questions': answered_questions,
        'testimonials': testimonials
        
    }
    return render(request, 'pages/about-us.html', context)


def privacy_policy(request):
    policies = PrivacyPolicy.objects.filter(active=True)
    context = {
        'policies': policies
    }
    return render(request, 'pages/privacy-policy.html', context)


@login_required
def policy_create(request):
    form = PrivacyPolicyForm()
    if request.method == 'POST':
        form = PrivacyPolicyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('pages:policies')
    context = {
        'form': form
    }
    return render(request, 'pages/privacy-policy-create-form.html', context)


@login_required
def policies(request):
    policies = PrivacyPolicy.objects.all()
    context = {
        'policies': policies
    }
    return render(request, 'pages/policies.html', context)


@login_required
def policy_edit(request, id):
    instance = PrivacyPolicy.objects.get(id = id)
    form = PrivacyPolicyEditForm(instance=instance)
    if request.method == 'POST':
        form = PrivacyPolicyEditForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfull.')
            return redirect('pages:policies')
        else:
             messages.error(request, 'Invalid form')
    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'pages/privacy-policy-edit-form.html', context)


@login_required
def terms(request):
    terms = TermsAndCondition.objects.filter(active=True)
    context = {
        'terms': terms
    }
    return render(request, 'pages/terms.html', context)


def t_and_c(request):
    terms = TermsAndCondition.objects.filter(active=True)
    context = {
        'terms': terms
    }
    return render(request, 'pages/terms-and-conditions.html', context)


@login_required
def terms_create(request):
    form = TermsAndConditionForm()
    if request.method == 'POST':
        form = TermsAndConditionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('pages:terms')
    context = {
        'form': form
    }
    return render(request, 'pages/terms-create-form.html', context)


@login_required
def terms_edit(request, id):
    instance = TermsAndCondition.objects.get(id = id)
    form = TermsAndConditionEditForm(instance=instance)
    if request.method == 'POST':
        form = TermsAndConditionEditForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfull.')
            return redirect('pages:terms')
        else:
             messages.error(request, 'Invalid form')
    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'pages/terms-edit-form.html', context)


@login_required
def service_create(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('pages:services-list')
    context = {
        'form': form
    }
    return render(request, 'pages/service-create-form.html', context)


@login_required
def services_list(request):
    services = Service.objects.order_by("-created_date")
    context = {
        'services': services
    }
    return render(request, 'pages/services-list.html', context)


def services(request):
    services = Service.objects.order_by("-created_date").filter(active=True)
    context = {
        'services': services
    }
    return render(request, 'pages/services.html', context)


def service_details(request, id):
    service = get_object_or_404(Service, id=id)
    context = {
        'service': service
    }
    return render(request, 'pages/service-details.html', context)


@login_required
def service_edit(request, id):
    instance = Service.objects.get(id = id)
    form = ServiceEditForm(instance=instance)
    if request.method == 'POST':
        form = ServiceEditForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfull.')
            return redirect('pages:services-list')
        else:
             messages.error(request, 'Invalid form')
    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'pages/service-edit-form.html', context)


def team(request):
    team = Team.objects.filter(active = True)
    context = {
        'team':team
    }
    return render(request, "pages/team.html", context)


def team_member_details(request, member_id):
    team_member = get_object_or_404(Team,member_id =member_id)
    context = {
        'team_member': team_member
    }
    return render(request, "pages/team-details.html", context)


@login_required
def testimonial_form(request):
    clients = Testimonial.objects.all()
    form = TestimonialForm()
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.client = request.user
            form_instance.save()
            messages.success(request, 'Thank you for your feedback.')
            return redirect('pages:testimonial-form')
        else:
             messages.error(request, 'Form invalid')
    context = {
        'form': form,
        'clients': clients
    }
    return render(request, 'pages/testimonial-form.html', context)