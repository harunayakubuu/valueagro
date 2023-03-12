from django.urls import path
from . views import (
    ProcurementRequestsList,
    ProcurementRequestCreate,
    ProcurementRequestUpdate,
    delete_procurement_item,
    procurement_chairman_approval,
    procurement_md_approval,
    procurement_request_details,
    ProcurementRequestDeleteView
)

app_name = 'procurements'

urlpatterns = [
    path('requests', ProcurementRequestsList.as_view(), name='procurement-requests'),
    
    path('form/', ProcurementRequestCreate.as_view(), name='procurement-request-create'),
    path('<int:id>/details/', procurement_request_details, name='procurement-request-details'),
    path('<str:pk>/update/', ProcurementRequestUpdate.as_view(), name='procurement-request-update'),
    path('<int:pk>/item/delete/', delete_procurement_item, name='delete-procurement-item'),
    path('<int:id>/chairman/approval/', procurement_chairman_approval, name='procurement-chairman-approval'),
    path('<int:id>/md/approval/', procurement_md_approval, name='procurement-md-approval'),
    path('<int:pk>/delete/', ProcurementRequestDeleteView.as_view(), name='procurement-request-delete'),
]