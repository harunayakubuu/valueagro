from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .truck import Truck
from products.models import Product
# from decimal import Decimal


def truck_add(request):
    truck = Truck(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        delivery_address = str(request.POST.get('deliveryaddress'))
        product = get_object_or_404(Product, id = product_id)
        truck.add(product = product, qty=product_qty, addr=delivery_address)

        truckqty = truck.__len__()
        response = JsonResponse({'qty': truckqty, 'addr': delivery_address})
        return response


def truck_summary(request):
    truck = Truck(request)
    context = {
        'truck': truck,
    }
    return render(request, 'trucks/truck-summary.html', context)


def truck_update(request):
    truck = Truck(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        delivery_address = str(request.POST.get('deliveryaddress'))
        truck.update(product = product_id, qty=product_qty, address=delivery_address)

        truckqty = truck.__len__()
        trucktotal = truck.get_total_price()

        response = JsonResponse({'qty': truckqty, 'subtotal': trucktotal})
        return response
        

def truck_delete(request):
    truck = Truck(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        truck.delete(product = product_id)

        truckqty = truck.__len__()
        trucktotal = truck.get_total_price()
        response = JsonResponse({'qty': truckqty, 'subtotal': trucktotal})

        return response
