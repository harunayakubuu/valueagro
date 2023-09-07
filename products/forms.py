from django import forms
from django.forms import inlineformset_factory
from .models import (
    Product, MarketAgentProduct, ProductType, 
    ProductVariety, ProductAttribute, ProductSpecification,
    ProductPicture
)


class MarketAgentProductCreateForm(forms.ModelForm):
    class Meta:
        model = MarketAgentProduct
        fields =  (
            'zone', 
            'state', 
            'local_government_area', 
            'market_name', 
            'market_type', 
            'market_days',
            'product_name',
            'category',
            'product_type',
            'product_variety',
            'product_quality',
            'price',
            'price_unit',
            'main_picture',
            'video',
            'description',
        )

        widgets = {
            'zone': forms.Select(attrs = {'class': 'form-select'}),
            'state': forms.Select(attrs = {'class': 'form-select'}),
            'local_government_area': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Local Government Area'}),
            'market_name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Market name'}),
            'market_type': forms.Select(attrs = {'class': 'form-select'}),
            'market_days': forms.Select(attrs = {'class': 'form-select'}),
            'product_name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Product name'}),
            'category': forms.Select(attrs = {'class': 'form-select'}),
            'product_type': forms.Select(attrs = {'class': 'form-select'}),
            'product_variety': forms.Select(attrs = {'class': 'form-select'}),
            'product_quality': forms.Select(attrs = {'class': 'form-select'}),
            'price_unit': forms.Select(attrs = {'class': 'form-select'}),
            'main_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),#'accept': '.mp4'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Product description', 'rows':'4'}),
        }




class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'product_type', 'product_variety', 'price', 'price_unit', 'main_picture', 'description', 'available'] 

        labels = {
            'product_name': 'Product Name',
            'category': 'Category',
            'product_type': 'Product Type',
            'product_variety': 'Product Variety',
            'price': 'Asking Price',
            'price_unit': 'Product Price Unit',
            'description': 'Product Description',
            'main_picture': 'Product Main Picture',            
            'availble': 'Product Availability',
        }
        
        widgets = {
            'product_name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Product name'}),
            'category': forms.Select(attrs = {'class': 'form-select'}),
            'product_type': forms.Select(attrs = {'class': 'form-select'}),
            'product_variety': forms.Select(attrs = {'class': 'form-select'}),
            'price': forms.NumberInput(attrs = {'class': 'form-control'}),
            'price_unit': forms.Select(attrs = {'class': 'form-select'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Product description', 'rows':'4'})
        }

class ProductSpecificationForm(forms.ModelForm):
    class Meta:
        model = ProductSpecification
        fields = ['attribute', 'value'] 

        labels = {
            'attribute': 'Product Attribute',
        }
        
        widgets = {
            'attribute': forms.Select(attrs = {'class': 'form-select'}),
            'value': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Attribute value'}),
        }

class ProductPictureForm(forms.ModelForm):
    class Meta:
        model = ProductPicture
        fields = ['name', 'picture'] 

        labels = {
            'name': 'Picture Name',
        }
        
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Picture name'}),
        }


ProductSpecificationFormFormSet = inlineformset_factory(
    Product, ProductSpecification, form=ProductSpecificationForm,
    extra=1, can_delete=True, can_delete_extra=True
)

ProductPictureFormFormSet = inlineformset_factory(
    Product, ProductPicture, form=ProductPictureForm,
    extra=1, can_delete=True, can_delete_extra=True
)


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product        
        fields = ['product_name', 'category', 'product_type', 'product_variety', 'price', 'price_unit', 'main_picture', 'description', 'available'] 

        labels = {
            'product_name': 'Product Name',
            'category': 'Category',
            'product_type': 'Product Type',
            'product_variety': 'Product Variety',
            'price': 'Asking Price',
            'price_unit': 'Product Price Unit',
            'description': 'Product Description',
            'main_picture': 'Product Main Picture',            
            'availble': 'Product Availability',
        }
        
        widgets = {
            'product_name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Product name'}),
            'category': forms.Select(attrs = {'class': 'form-select'}),
            'product_type': forms.Select(attrs = {'class': 'form-select'}),
            'product_variety': forms.Select(attrs = {'class': 'form-select'}),
            # 'price': forms.Select(attrs = {'class': 'form-select'}),
            'price_unit': forms.Select(attrs = {'class': 'form-select'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Product description', 'rows':'4'})
        }