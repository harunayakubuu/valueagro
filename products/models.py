import uuid
import random
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from .choices import STATE_CHOICES
from mptt.models import MPTTModel, TreeForeignKey

import json
from json import JSONEncoder

from django.core.exceptions import ValidationError
# import magic

Account = settings.AUTH_USER_MODEL


# Validates User Uploaded Files
# def validate_file_mimetype(file):
#     accept = ['video/mp4']
#     file_mime_type = magic.from_buffer(file.read(1024), mime=True)
#     print(file_mime_type)
#     if file_mime_type not in accept:
#         raise ValidationError("Unsupported file format")


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True, verbose_name ='Category Name')
    slug = models.SlugField(max_length=255, unique=True)
    active = models.BooleanField("Active", default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:public_product_list_by_category', args=[str(self.slug)])


class ProductBase(models.Model):
    category        = models.ForeignKey(Category, on_delete = models.CASCADE)
    product_type    = models.ForeignKey('ProductType', verbose_name="Product Type", on_delete = models.DO_NOTHING)
    product_variety = models.ForeignKey('ProductVariety', verbose_name="Variety", on_delete = models.DO_NOTHING)
    product_name    = models.CharField(verbose_name='Product name', max_length = 255)
    main_picture    = models.ImageField(upload_to = "pictures/products", help_text = "Width:600px X Height:600px")
    description     = models.TextField(blank=True, null=True)
    
    slug            = models.SlugField(unique=True, blank = True, null = True)
    
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True
    

class Product(ProductBase):
    # id              = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False
    price           = models.PositiveIntegerField(verbose_name="Offering_price")
    PRICE_UNIT_CHOICES = (
        ('KG', 'Kg'),
        ('50KG', '50 Kg'),
        ('LITRE', 'Litre'),
        ('TONN', 'Tonn'),
    )
    price_unit      = models.CharField(max_length = 20, choices = PRICE_UNIT_CHOICES, default = 'Tonn')
    available       = models.BooleanField("Available", default=True)
    public          = models.BooleanField("Public", default=True, help_text="Check this box for the product to go public.")
    
    author          = models.ForeignKey(Account, on_delete = models.SET_NULL, blank = True, null = True)

    class Meta:
        ordering = ('-created_at',)
        # index_together = (('id', 'slug'),)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.product_name}-{self.created_at.strftime('%d/%m/%Y')}"

    def get_absolute_url(self):
        return reverse('products:public-product-details', args=[(self.id)])

    def get_product_details(self):
        return reverse('products:p-details', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def slugify_instance_product_name(instance, save=False, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.product_name)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = random.randint(1_000_000, 2_000_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_product_name(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def product_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
       slugify_instance_product_name(instance, save=False)

pre_save.connect(product_pre_save, sender = Product)

def product_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_product_name(instance, save=True)
        
post_save.connect(product_post_save, sender = Product)


class ProductEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Picture(models.Model):
    name = models.CharField(max_length=50, blank = True, null = True)
    picture = models.ImageField(upload_to = 'pictures/products/pictures', blank = True, null = True, help_text = "Width:600px X Height:000px")
    
    class Meta:
        abstract = True
        verbose_name = 'Product Pictures'
        verbose_name_plural = 'Product Pictures'

    def __str__(self):
        return str(self.name)
    

class ProductPicture(Picture):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    
    class Meta:
        verbose_name = 'Product Pictures'
        verbose_name_plural = 'Product Pictures'

    def __str__(self):
        return str(self.product.product_name)
    

class MarketAgentProductPicture(Picture):
    product = models.ForeignKey('MarketAgentProduct', on_delete = models.CASCADE)
    
    class Meta:
        verbose_name = 'Agent Product Picture'
        verbose_name_plural = 'Agent Product Pictures'

    def __str__(self):
        return str(self.name)
        

class ProductType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_types')
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'

    def __str__(self):
        return str(self.name)


class ProductVariety(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='product_variety')
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Product Variety'
        verbose_name_plural = 'Product Variety'

    def __str__(self):
        return str(self.name)


class ProductAttribute(models.Model):
    product_variety = models.ForeignKey(ProductVariety, verbose_name = "Product type", on_delete=models.CASCADE)
    name = models.CharField("Attribute name", max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, verbose_name = "Product", on_delete = models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, verbose_name = 'Specification', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name = 'Value', blank=True, null = True)

    def __str__(self):
        return f'{self.attribute} - {self.value}'

    class Meta:
        verbose_name = "Product Specification"
        verbose_name_plural = "Product Specifications"

    def get_absolut_url(self):
        return self.product.get_absolute_url()


class MarketAgentProduct(ProductBase):
    agent = models.ForeignKey(Account, on_delete = models.DO_NOTHING)
    ZONE_CHOICES = (
        ('NE', 'North-East'),
        ('NW', 'North-West'),
        ('NC', 'North-Central'),
        ('SE', 'South-East'),
        ('SW', 'South-West'),
        ('SS', 'South-South'),
    )
    zone = models.CharField(max_length = 2, choices = ZONE_CHOICES)
    state = models.CharField(max_length = 10, choices = STATE_CHOICES)
    local_government_area = models.CharField(max_length = 50)
    market_name = models.CharField(max_length = 50, unique = True)
    MARKET_TYPE_CHOICES = (
        ('Weekly', 'Weekly'),
        ('Daily', 'Daily'),
    )
    market_type = models.CharField(max_length = 6, choices = MARKET_TYPE_CHOICES)
    MARKET_DAYS_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Everyday', 'Everyday'),
    )
    market_days = models.CharField(max_length = 9, choices = MARKET_DAYS_CHOICES)
    
    PRODUCT_QUALITY_CHOICES = (
        ('1', 'Grade 1'),
        ('2', 'Grade 2'),
        ('3', 'Grade 3'),
        ('4', 'Grade 4'),
        ('5', 'Grade 5'),
    )
    product_quality = models.CharField(max_length = 1, choices = PRODUCT_QUALITY_CHOICES)
    price = models.DecimalField(max_digits = 15, decimal_places = 2, help_text = "Price per tonn")
    PRICE_UNIT_CHOICES = (
        ('KG', 'Kg.'),
        ('50KG', '50Kg'),
        ('BAG40', 'Bag (40 measure)'),
        ('TONN', 'Tonn'),
    )
    price_unit = models.CharField(max_length = 30, choices = PRICE_UNIT_CHOICES, default = 'Tonn')
    video = models.FileField(upload_to = "media/videos/market-products", blank=True, null=True)#, validators=[validate_file_mimetype])
    location = models.CharField(max_length = 200)
    
    def __str__(self):
        return f'{ self.location }, {str(self.agent.username)} - {str(self.market_name)}'

    class Meta:
        verbose_name = 'Market Product'
        verbose_name_plural = 'Market Products'

def slugify_instance_agent_product_name(instance, save=False, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.product_name)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = random.randint(1_000_000, 2_000_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_agent_product_name(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def agent_product_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
       slugify_instance_agent_product_name(instance, save=False)

pre_save.connect(agent_product_pre_save, sender = MarketAgentProduct)

def agent_product_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_agent_product_name(instance, save=True)
        
post_save.connect(agent_product_post_save, sender = MarketAgentProduct)



class MarketProductPicture(models.Model):
    market_product = models.ForeignKey(Product, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to = 'pictures/market-products/pictures/%Y%m%d')
    
    class Meta:
        verbose_name = 'Product Pictures'
        verbose_name_plural = 'Product Pictures'

    def __str__(self):
        return str(self.name)