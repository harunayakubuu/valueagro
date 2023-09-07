from django import forms
from .models import Order, Payment


class OrderPaymentForm(forms.ModelForm):
    amount = forms.IntegerField(
        widget = forms.NumberInput(attrs = {'class': 'form-control mb-3'})
    )
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Payment
        fields = ['amount', 'payment_status', 'payment_date']


class OrderUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['order_status']
