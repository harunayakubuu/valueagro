from django.db import models
from django.conf import settings


Account = settings.AUTH_USER_MODEL


class ProcurementRequest(models.Model):
    # user = models.ForeignKey(Account, on_delete = models.SET_NULL, blank = True, null = True)
    title =  models.CharField(max_length = 100)
    procurement_request_description = models.TextField(help_text = 'Give the general information on this request.')

    MD_APPROVAL_STATUS = (
        ('Pending', "Pending"),
        ('Approved', "Approved"),
        ('Declined', "Declined"),
    )
    md_approval_status = models.CharField(max_length = 10, choices = MD_APPROVAL_STATUS, default='Pending')
    md_comment = models.TextField(blank = True, null = True)

    CHAIRMAN_APPROVAL_STATUS = (
        ('Pending', "Pending"),
        ('Approved', "Approved"),
        ('Declined', "Declined"),
    )
    chairman_approval_status = models.CharField(max_length = 10, choices = CHAIRMAN_APPROVAL_STATUS, default='Pending')
    chairman_comment = models.TextField(blank = True, null = True)

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Procurement Request'
        verbose_name_plural = 'Procurement Requests'


class ProcurementItem(models.Model):
    procurement_request = models.ForeignKey(ProcurementRequest, on_delete = models.CASCADE)
    item_name = models.CharField("Name of Item", max_length = 100)
    description = models.TextField("Item description")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    reason_for_item_need = models.CharField(max_length = 255, help_text = "Give the reasons why this item is needed")

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity_needed
        return super().save(*args, **kwargs)

    # class Meta:
    #     verbose_name = 'Procurement Request'
    #     verbose_name_plural = 'Procurement Requests'