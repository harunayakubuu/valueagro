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

from .forms import (
    ProductCreateForm, ProductEditForm, 
    MarketAgentProductCreateForm, ProductPictureFormFormSet,
    ProductSpecificationFormFormSet
)
from .models import Product, MarketAgentProduct, Category, ProductPicture, ProductSpecification

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView


from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


#Public
def public_products(request, category_slug=None):
    
    category = None
    categories = Category.objects.all()
    
    products = Product.objects.order_by('-created_at').filter(available = True)

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

    product = get_object_or_404(Product, id=id, available=True)

    context = {
        'product': product,
    }
    return render(request, 'products/public-product-details.html', context)


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
def market_agent_products_list(request):
    agent_products = MarketAgentProduct.objects.filter(agent=request.user)
    context = {
        'agent_products': agent_products
    }
    return render(request, 'products/market-agent-products-list.html', context)


@login_required
def market_agent_product_details(request, id):
    product = MarketAgentProduct.objects.get(id=id)
    context = {
        'product': product,
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
            messages.success(request, 'Product saved')

            return redirect("products:market-agent-products-list")
    context = {
        'form': form,
    }
    return render(request, 'products/market-agent-product-edit.html', context)


class MarketAgentProductDeleteView(LoginRequiredMixin, DeleteView):
    model = MarketAgentProduct
    template_name = 'products/product-delete.html'
    success_url = reverse_lazy('products:products-list-admin')


@login_required
def market_agent_products_all(request):
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
    return render(request, "products/product-details-admin.html", context)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product-delete.html'
    success_url = reverse_lazy('products:products-list-admin')


import csv
import datetime

def get_csv_file(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename = "market_produts.csv"'
    products = MarketAgentProduct.objects.order_by('product_variety').order_by('-created_at')
    
    writer = csv.writer(response)
    writer.writerow(['Agent', 'Zone', 'State', 'Local Government', 'Market', 'Market Type', 'Market Day(s)', 'Product', 'Product Type', 'Product Category', 'Product Variety', 'Product Quality', 'Product Price', 'Price Unit', 'Date'])
    for product in products:
        # if not product.created_at < datetime.date.today():
        writer.writerow([
            product.agent, product.zone,
            product.state, product.local_government_area,
            product.market_name, product.market_type,
            product.market_days, product.product_name,
            product.category, product.product_type,
            product.product_variety, product.product_quality,
            product.price, product.price_unit,
            product.created_at.strftime('%d/%m/%Y')
        ])
    return response