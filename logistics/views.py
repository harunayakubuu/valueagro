from django.shortcuts import render, redirect
from . forms import DriverForm, VehicleForm
from . models import Driver, Vehicle

from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import DeleteView


def fleet_management(request):
    vehicles = Vehicle.objects.all()

    context = {
        'vehicles': vehicles,
    }
    return render(request, 'logistics/fleet-management.html', context)


def vehicle_register(request):
    form = VehicleForm()
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('logistics:fleet-management')
    context = {
        'form': form,
    }
    return render(request, 'logistics/vehicle-register.html', context)


def vehicle_edit(request, id):
    instance = Vehicle.objects.get(id = id)
    form = VehicleForm(instance = instance)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance = instance)
        if form.is_valid():
            form.save()
            return redirect('logistics:fleet-management')
    context = {
        'form': form,
    }
    return render(request, 'logistics/vehicle-edit.html', context)


def vehicle_details(request, id):
    vehicle = Vehicle.objects.get(id = id)
    context = {
        'vehicle': vehicle,
    }
    return render(request, 'logistics/vehicle-details.html', context)


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'logistics/vehicle-delete.html'
    success_url = reverse_lazy('logistics:fleet-management')


def driver_management(request):
    drivers = Driver.objects.all()

    context = {
        'drivers': drivers,
    }
    return render(request, 'logistics/driver-management.html', context)


def driver_register(request):
    form = DriverForm()
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('logistics:driver-management')
    context = {
        'form': form,
    }
    return render(request, 'logistics/driver-register.html', context)


def driver_edit(request, id):
    instance = Driver.objects.get(id = id)
    form = DriverForm(instance = instance)
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance = instance)
        if form.is_valid():
            form.save()
            return redirect('logistics:driver-management')
    context = {
        'form': form,
    }
    return render(request, 'logistics/driver-edit.html', context)


def driver_details(request, id):
    driver = Driver.objects.get(id = id)
    context = {
        'driver': driver,
    }
    return render(request, 'logistics/driver-details.html', context)


class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = Driver
    template_name = 'logistics/driver-delete.html'
    success_url = reverse_lazy('logistics:driver-management')


