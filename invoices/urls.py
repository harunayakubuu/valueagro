from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    # path('invoice/pdf/', views.invoice_pdf, name = 'invoice_pdf'),
    path('export/excel/', views.export_excel, name = 'export_excel'),
]