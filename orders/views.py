from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from trucks.truck import Truck
from accounts.models import Account
from .forms import OrderPaymentForm, OrderUpdateForm
from .models import Order, OrderItem
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

#xhtml2PDF imports
# import os
# from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# from django.contrib.staticfiles import finders



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
    
    # subject = "Order Placed"
    # message = f"Your order with ID ({ order_id }) has been placed."
    # send_mail(
    #         subject,
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         user_email,
    #         fail_silently = False
    #     )

    # messages.success(request, "Order placed successfully")
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


def order_pdf_view(request, *args, **kwargs):
    
    transaction_id = kwargs.get('transaction_id')
    order = get_object_or_404(Order, transaction_id = transaction_id)
    order_items = OrderItem.objects.filter(order=order)

    template_path = 'orders/pdf2.html'
    context = {
        'order': order,
        'items': order_items
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    # For direct download
    # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    
    # for displaying in browser before downloading
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf_view(request):
    template_path = 'orders/pdf1.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # For direct download
    # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    # for displaying in browser before downloading
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response