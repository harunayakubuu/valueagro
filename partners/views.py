from django.shortcuts import render, redirect, get_object_or_404
from .models import Partner
from .forms import PartnerForm

from django.contrib import messages



def partner_list(request):

    context = {

    }
    return render(request, 'partners/partner-list.html', context)


def partner_create(request):
    form = PartnerForm()
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            form.save(commit = False)
            messages.success(request, "Parnter saved.")
            return redirect('partners:partner-list')
    context = {

    }
    return render(request, 'partners/partner-form.html', context)


def partners(request):
    partners = Partner.objects.filter(active = True).order_by('name')
    context = {
        'partners': partners
    }
    return render(request, 'partners/partners.html', context)


def partner_details(request, slug):
    partner = get_object_or_404(Partner, slug = slug)
    context = {
        'partner': partner
    }
    return render(request, 'partners/partner-details.html', context)


def partner_edit(request):

    context = {

    }
    return render(request, 'partners/partner-edit.html', context)


def partner_delete(request):

    context = {

    }
    return render(request, 'partners/partner-delete.html', context)