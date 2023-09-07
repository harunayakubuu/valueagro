from django.shortcuts import render, redirect, get_object_or_404
from .models import DeliveryAddress
from .forms import AddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def addresses(request):
    addresses = DeliveryAddress.objects.filter(user = request.user.profile)
    context = {
        'addresses': addresses
    }
    return render(request, 'addresses/addresses.html', context)


@login_required
def address_add(request):
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            temp = form.save(commit = False)
            temp.user = request.user.profile
            temp.save()
            messages.success(request, "Saved")
            return redirect("addresses:address-list")
    context = {
        'form': form
    }
    return render(request, 'addresses/address-add.html', context)


@login_required
def address_edit(request, id):
    address = get_object_or_404(DeliveryAddress, id = id)
    form = AddressForm(instance = address)
    if request.method == "POST":
        form = AddressForm(request.POST, instance = address)
        if form.is_valid():
            form.save()
            messages.success(request, "Saved")
            return redirect("addresses:address-list")    
    context = {
        'form': form
    }
    return render(request, 'addresses/address-edit.html', context)


@login_required
def address_delete(request, id):
    address = get_object_or_404(DeliveryAddress, id = id)
    address.delete()
    return redirect("addresses:address-list")