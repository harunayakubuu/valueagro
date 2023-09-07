from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Faq
from .forms import FaqForm, FaqEditForm


def faqs(request):
    faqs = Faq.objects.order_by('-created_at').filter(active=True)
    paginator = Paginator(faqs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'faqs/faqs.html', context)


@login_required
def all_faqs(request):
    all_faqs = Faq.objects.order_by('-created_at')
    context = {
        'all_faqs': all_faqs
    }
    return render(request, 'faqs/faqs-all.html', context)


@login_required
def faqs_create(request):
    form = FaqForm()
    if request.method == 'POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('faqs:faqs-all')
    context = {
        'form': form
    }
    return render(request, 'faqs/faqs-create-form.html', context)


@login_required
def faqs_edit(request, id):
    instance = Faq.objects.get(id = id)
    form = FaqEditForm(instance=instance)
    if request.method == 'POST':
        form = FaqEditForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfull.')
            return redirect('faqs:faqs-all')
        else:
             messages.error(request, 'Form invalid')
    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'faqs/faqs-edit-form.html', context)


@login_required
def faqs_delete(request, id):
    faq = get_object_or_404(Faq, id=id)
    faq.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('faqs:faqs-all')