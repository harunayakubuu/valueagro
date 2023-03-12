import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


class Driver(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = PhoneNumberField(verbose_name="Phone number")
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
        ('Disengaged', 'Disengaged'),
    )
    date_of_birth = models.DateField()
    driver_license = models.FileField()
    picture = models.ImageField(upload_to = "Pictures/Drivers")
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default='Active')  

    def __str__(self):
        return self.name

    def get_driver_details(self):
        return reverse('logistics:driver-details', args=[str(self.id)])

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'


class Category(models.Model):
    name =  models.CharField(max_length = 100)
    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Vehicle(models.Model):
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, blank = True, null = True)
    vehicle_number = models.CharField(max_length = 10, unique = True)
    chasis_number = models.CharField(max_length = 30, unique = True)
    driver = models.OneToOneField(Driver, blank = True, null = True, on_delete = models.SET_NULL)
    STATUS_CHOICES = (
        ('AR', 'Active and Ready'),
        ('AB', 'Active and Busy'),
        ('BD', 'Broken Down'),
        ('UM', 'Undergoing Repairs'),
        ('UR', 'Undergoing Maintenance'),
    )
    picture = models.ImageField(upload_to = "Pictures/Vehicle")
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default='Active')  

    def __str__(self):
        return self.vehicle_number

    def get_vehicle_details(self):
        return reverse('logistics:vehicle-details', args=[str(self.id)])

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'


class Delivery(models.Model):
    delivery_id = models.CharField(max_length = 20)
    # order = models.ForeignKey(Order, on_delete = models.CASCADE)
    verhicle = models.ForeignKey(Vehicle, on_delete = models.CASCADE)
    delivery_address = models.CharField(max_length = 100)
    pickup_date = models.DateField()
    expected_delivery_date = models.DateField()
    transportation_charges = models.DecimalField(max_digits = 10, decimal_places = 2)
    STATE_CHOICES = (
        ('TOOKOFF', 'Took off'),
        ('ONWAY', 'On the way'),
        ('ARRIVED', 'Arrived'),
        ('UNLOADING', 'Unloading'),
        ('DELIVERED', 'Delivered'),
    )
    delivary_status = models.CharField(max_length = 15)
    
    def __str__(self):
        return self.delivery_id

    # def save(self, *args, **kwargs):
    #     if self.order_id == '':
    #         self.order_id = code = str(uuid.uuid4()).upper().split('-')[4]

    #     if self.created == None:
    #         self.created = timezone.now()
            
    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'