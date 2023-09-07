from products.models import Product
from django.conf import settings
import json


class Truck():

    def __init__(self, request):
        self.session = request.session
        # truck = self.session.get(settings.TRUCK_SESSION_ID)
        truck = self.session.get('skey')
        if 'skey' not in request.session:
            truck = self.session['skey'] = {}
        self.truck = truck


    def add(self, product, qty, addr):
        product_id = product.id
        if product_id in self.truck:
            self.truck[product_id]['qty'] = qty
            self.truck[product_id]['address'] = address
        else:
            self.truck[product_id] = {'price': int(product.price), 'qty': int(qty), 'addr': str(addr)}
        self.save()


    def delete(self, product):
        """
        Delete product from session data
        """
        product_id = str(product)
        if product_id in self.truck:
            del self.truck[product_id]
            self.save()

    
    def update(self, product, qty, address):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.truck:
            self.truck[product_id]['qty'] = qty
            self.truck[product_id]['address'] = address
        self.save()


    def __iter__(self):
        product_ids = self.truck.keys()
        products = Product.objects.filter(id__in = product_ids)
        truck = self.truck.copy()

        for product in products:
            truck[str(product.id)]['product'] = product

        for item in truck.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item


    def __len__(self):
        """
        Get the truck data and count the quantity of items in the truck
        """
        return sum(int(item['qty']) for item in self.truck.values())


    def get_total_price(self):
        # truck_size = 0
        # if 
        return sum(item['price'] * int(item['qty']) for item in self.truck.values())


    def save(self):
        self.session.modified = True

    
    def clear(self):
        del self.session[settings.TRUCK_SESSION_ID]
        self.save()
