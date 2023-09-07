from pyexpat import model
from django.contrib import admin
from .models import (
    Category, Product,
    MarketAgentProduct,
    ProductType,
    ProductVariety,
    ProductPicture,
    MarketAgentProductPicture,
    ProductSpecification,
    ProductAttribute
)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(ProductType, ProductTypeAdmin)


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductVarietyAdmin(admin.ModelAdmin):
    inlines = [
        ProductAttributeInline
    ]
    list_display = ['product_type', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(ProductVariety, ProductVarietyAdmin)


class ProductPictureInline(admin.TabularInline):
    model = ProductPicture
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductPictureInline,
        ProductSpecificationInline
    ]

    list_display = ['product_name', 'price', 'available']
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)


class MarketAgentProductPictureInline(admin.TabularInline):
    model = MarketAgentProductPicture
    extra = 1

class MarketAgentProductAdmin(admin.ModelAdmin):
    inlines = [
        MarketAgentProductPictureInline
    ]
    list_display = ['product_name', 'price']
    prepopulated_fields = {'slug': ('product_name',)}
admin.site.register(MarketAgentProduct, MarketAgentProductAdmin)
