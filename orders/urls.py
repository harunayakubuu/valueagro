from django.urls import path
from . views import (
    order_add, place_order, orders_list,
    order_details, order_placed, my_orders,
    order_payments, order_update, render_pdf_view, order_pdf_view
)

app_name = 'orders'


urlpatterns = [
    path('list/', orders_list, name = 'orders-list'),

    path('invoice/', render_pdf_view, name = 'invoice'),
    path('invoice/<transaction_id>/', order_pdf_view, name = 'order_pdf_view'),

    path('order/add/', order_add, name = 'order-add'),
    path('order/placed/', order_placed, name = 'order-placed'),
    path('order<str:transaction_id>/edit/', order_update, name = 'order-edit'),
    path('order/<str:transaction_id>/', order_details, name = 'order-details'),
    path('my-orders/', my_orders, name = 'my-orders'),
    path('place-order/', place_order, name = 'place-order'),
    path('<str:transaction_id>/payments/', order_payments, name = 'order-payments'),

]