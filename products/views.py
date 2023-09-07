# Import for Image Meta data extraction
import datetime
import os
from PIL import Image
from PIL.ExifTags import TAGS

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from .filters import ProductFilter
from .utils import get_geo

from .forms import (
    ProductCreateForm, ProductEditForm, 
    MarketAgentProductCreateForm, ProductPictureFormFormSet,
    ProductSpecificationFormFormSet
)
from .models import Product, MarketAgentProduct, Category, ProductPicture, ProductSpecification

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

import xlwt
import folium

from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


#Public
def public_products(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.order_by('-created_at').filter(available = True, public = True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'products/public-products.html', context)


# Public
def public_product_details(request, id):
    product = get_object_or_404(Product, id=id, available=True, public = True)
    context = {
        'product': product,
    }
    return render(request, 'products/public-product-details.html', context)


# This view handles the form that submits products by market agents
@login_required
def market_agent_product_create(request):
    form = MarketAgentProductCreateForm()
    if request.method == 'POST':
        form = MarketAgentProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.agent = request.user
            obj.save()
            messages.success(request, 'Product saved')

            return redirect("products:market-agent-products-list")
    context = {
        'form': form,
    }
    return render(request, 'products/market-agent-product-create.html', context)


@login_required
def admin_market_agent_products(request, agent):
    agent_products = MarketAgentProduct.objects.filter(agent__username=agent)
    context = {
        'agent_products': agent_products
    }
    return render(request, 'products/admin_market_agent_products.html', context)



# This view lists all products sent by an agent to the agent
# The agent sees the list of products he sent
@login_required
def market_agent_products_list(request):
    agent_products = MarketAgentProduct.objects.filter(agent=request.user)
    context = {
        'agent_products': agent_products
    }
    return render(request, 'products/market-agent-products-list.html', context)


@login_required
def market_agent_product_details(request, id):
    product = MarketAgentProduct.objects.get(id=id)

    img = product.main_picture
    print(img)
    location = [11.962244, 8.502598]
    m = folium.Map(location=location, zoom_start=7, Tooltip="View more info.")
    folium.Marker(location = location, icon=folium.Icon(color='blue')).add_to(m)
    m = m._repr_html_()

    context = {
        'product': product,
        'map': m,
    }
    return render(request, 'products/market-agent-product-details.html', context)


@login_required
def market_agent_product_edit(request, id):
    instance = MarketAgentProduct.objects.get(id=id)
    form = MarketAgentProductCreateForm(instance=instance)
    if request.method == 'POST':
        form = MarketAgentProductCreateForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved')

            return redirect("products:market-agent-products-list")
    context = {
        'form': form,
    }
    return render(request, 'products/market-agent-product-edit.html', context)


class MarketAgentProductDeleteView(LoginRequiredMixin, DeleteView):
    model = MarketAgentProduct
    template_name = 'products/admin_product_delete.html'
    success_url = reverse_lazy('products:products-list-admin')


@login_required
def market_agents_products_all(request):
    all_market_agent_products = MarketAgentProduct.objects.all()
    context = {
        'all_market_agent_products': all_market_agent_products,
    }
    return render(request, 'products/all-market-agent-products.html', context)


class ProductInline():
    form_class = ProductCreateForm
    model = Product
    template_name = "products/product_create_or_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('products:products-list-all')
    
    def formset_specifications_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        specifications = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for specification in specifications:
            specification.product = self.object
            specification.save()

    
    def formset_pictures_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        pictures = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for picture in pictures:
            picture.product = self.object
            picture.save()

# Done
class ProductCreate(ProductInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'specifications': ProductSpecificationFormFormSet(prefix='specifications'),
                'pictures': ProductPictureFormFormSet(prefix='pictures'),
            }
        else:
            return {
                'specifications': ProductSpecificationFormFormSet(self.request.POST or None, self.request.FILES or None, prefix='specifications'),
                'pictures': ProductPictureFormFormSet(self.request.POST or None, self.request.FILES or None, prefix='pictures'),
            }


# Done
class ProductUpdate(ProductInline, UpdateView):
    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'specifications': ProductSpecificationFormFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='specifications'),
            'pictures': ProductPictureFormFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='pictures'),
        }


# Done
class ProductList(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

# done
def delete_picture(request, pk):
    try:
        picture = ProductPicture.objects.get(id=pk)
    except ProductPicture.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('products:update_product', pk=picture.product.id)

    picture.delete()
    messages.success(
            request, 'Picture deleted successfully'
            )
    return redirect('products:update_product', pk=picture.product.id)

# Done
def delete_specification(request, pk):
    try:
        specification = ProductSpecification.objects.get(id=pk)
    except ProductSpecification.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('products:update_product', pk=specification.product.id)

    specification.delete()
    messages.success(
            request, 'ProductSpecification deleted successfully'
            )
    return redirect('products:update_product', pk=specification.product.id)


@login_required
def product_details_admin(request, id):
    product = Product.objects.get(id = id)
    context = {
        'product': product,
    }
    return render(request, "products/admin_product_details.html", context)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/admin_product_delete.html'
    success_url = reverse_lazy('products:products-list-admin')


def get_excel_file(request):

    response = HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=Market Products '+str(datetime.date.today())+".xls"

    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet("Contacts Messages")

    row_num = 1

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Agent', 'Zone', 'State', 'Local Government', 'Market', 'Market Type', 'Market Day(s)', 'Product', 'Product Type', 'Product Category', 'Product Variety', 'Product Quality', 'Product Price', 'Description', 'Location', 'Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = products = MarketAgentProduct.objects.order_by('product_variety').order_by('-created_at').values_list('agent', 'zone', 'state', 'local_government_area', 'market_name', 'market_type', 'market_days', 'product_name', 'product_type', 'category', 'product_variety', 'product_quality', 'price', 'description', 'location', 'created_at')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)
    return response