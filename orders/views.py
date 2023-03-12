from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from trucks.truck import Truck
from accounts.models import Account
from .forms import OrderPaymentForm, OrderUpdateForm
from .models import Order, OrderItem
from django.contrib import messages


def place_order(request):
    return render(request, 'orders/place-order.html')


@login_required
def order_add(request):
    truck = Truck(request)
    user = Account.objects.get(username = request.user.username)
    order_session_id  = "785773300987888" #request.POST.get('sessionid')
    trucktotal = truck.get_total_price()
    order = Order.objects.create(
        user = user, amount = trucktotal, order_session_id = order_session_id
    )
    order_id = order
    for item in truck:
        OrderItem.objects.create(
            order = order_id, 
            product=item['product'], 
            price=item['price'],
            quantity = item['qty'],
            delivery_address = item['addr']
        )
    response = HttpResponse('success')
    return redirect('orders:order-placed')


def order_placed(request):
    truck = Truck(request)
    truck.clear()
    return render(request, 'orders/order-placed.html')


@login_required
def orders_list(request):
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'orders/orders-list.html', context)


@login_required
def user_orders(request):
    user = request.user
    orders = Order.objects.order_by('-created_date').filter(user = user)
    return orders

    # context = {
    #     'orders': orders
    # }
    # return render(request, 'orders/orders-list.html', context)

@login_required
def my_orders(request):
    orders = user_orders(request)
    context = {
        'orders': orders
    }
    return render(request, 'orders/my-orders.html', context)


@login_required
def order_details(request, transaction_id):

    order = get_object_or_404(Order, transaction_id = transaction_id)

    context = {
        'order': order
    }
    return render(request, 'orders/order-details.html', context)


@login_required
def order_update(request, transaction_id):
    order = get_object_or_404(Order, transaction_id = transaction_id)
    order_update_form = OrderUpdateForm(instance = order)
    if request.method == "POST":
        order_update_form = OrderUpdateForm(request.POST, instance = order)
        if order_update_form.is_valid():
            order_update_form.save()
            messages.success(request, "Changes saved")
            return redirect('orders:orders-list')

    context = {
        'order': order,
        'order_update_form':order_update_form
    }
    return render(request, 'orders/order-update.html', context)


@login_required
def order_delete(request):

    # orders = Order.objects.all()

    context = {

    }
    return render(request, 'orders/orders-list.html', context)


@login_required
def order_payments(request, transaction_id):
    order = get_object_or_404(Order, transaction_id = transaction_id)
    payment_form = OrderPaymentForm()
    if request.method == 'POST':
        payment_form = OrderPaymentForm(request.POST)
        if payment_form.is_valid():
            f = payment_form.save(commit = False)
            f.order = order
            
            f.save()
            messages.success(request, 'Payment information saved.')
            return redirect("orders:orders-list")

    context = {
        'order': order,
        "payment_form": payment_form
    }
    return render(request, 'orders/order-payments.html', context)