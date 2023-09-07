import uuid
import datetime
from django.db import models
from decimal import Decimal
from django.conf import settings

from products.models import Product


User = settings.AUTH_USER_MODEL


class Order(models.Model):
    order_session_id = models.CharField(max_length = 100, blank = True)
    transaction_id = models.CharField(max_length = 30, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'order_user')
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    
    ORDER_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Declined', 'Declined'),
        ('Processing', 'Processing'),
        ('Complete', 'Complete'),
    )
    order_status = models.CharField(max_length = 10, choices = ORDER_STATUS_CHOICES, default = 'Pending')
    delivery = models.BooleanField("Requires Delivery?", default = False)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_grand_total(self):
        order_delivery = self.order_delivery.all()
        if self.delivery:
            grand_total = self.amount
        else:
            grand_total = self.amount
        return grand_total

    # def save(self, *args, **kwargs):
    #     if self.transaction_id == '':
    #         self.transaction_id = code = str(uuid.uuid4()).upper().split('-')[4]
    #     return super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        t_id = str(datetime.datetime.now().timestamp())
        t_id = t_id.replace('.', '')
        if self.transaction_id == '':
            self.transaction_id = t_id
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('-created_date',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name = 'items', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, related_name = 'order_item', on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity = models.PositiveIntegerField(default = 1, help_text = "Quantity in trucks")

    delivery_address = models.CharField(max_length = 200, blank = True, null = True)

    @property
    def get_item_total_price(self):
        item_total_price = self.price * self.quantity
        return item_total_price



class OrderDelivery(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name="order_delivery")
    delivery_fee = models.PositiveIntegerField()
    PAYMENT_STATUS_CHOICES = (
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
    )
    payment_status = models.CharField(max_length = 10, choices = PAYMENT_STATUS_CHOICES, default = 'Unpaid')
    DELIVERY_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Arrived', 'Arrived'),
        ('Delivered', 'Delivered'),
    )
    delivery_status = models.CharField(max_length = 10, choices = DELIVERY_STATUS_CHOICES, default = 'Pending')

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{ str(self.order.transaction_id) }, { str(self.delivery_fee) }'

    
    class Meta:
        verbose_name_plural = "Delivery Info"
        verbose_name = "Delivery Info"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete = models.CASCADE, related_name="order_payment")
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    PAYMENT_STATUS_CHOICES = (
        ('Unpaid', 'Unpaid'),
        ('Failed', 'Failed'),
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    )
    payment_status = models.CharField(max_length = 10, choices = PAYMENT_STATUS_CHOICES, default = 'Unpaid')
    payment_date = models.DateTimeField()

    def __str__(self):
        return str(self.order.transaction_id)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
