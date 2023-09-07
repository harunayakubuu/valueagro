from django import forms
from django.forms import inlineformset_factory
from .models import ProcurementRequest, ProcurementItem



class ProcurementRequestCreateForm(forms.ModelForm):
    class Meta:
        model = ProcurementRequest
        fields = ['title','procurement_request_description',] 

        labels = {
            'title': 'Procurement Request Title',
            'procurement_request_description': 'Procurement Request Description',
        }
        
        widgets = {
            'description': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Procurement Request Description', 'rows':'4'})
        }



class MDProcurementRequestApprovalForm(forms.ModelForm):
    class Meta:
        model = ProcurementRequest
        fields = ['md_approval_status', 'md_comment'] 

        labels = {
            'md_approval_status': 'Approval',
            'md_comment': 'Comment',
        }
        
        widgets = {
            'md_approval_status': forms.Select(attrs = {'class': 'form-select'}),
            'md_comment': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Comment', 'rows':'4'})
        }



class ChairmanProcurementRequestApprovalForm(forms.ModelForm):
    class Meta:
        model = ProcurementRequest
        fields = ['chairman_approval_status', 'chairman_comment',] 

        labels = {
            'chairman_approval_status': 'Approval',
            'chairman_comment': 'Comment',
        }
        
        widgets = {
            'chairman_approval_status': forms.Select(attrs = {'class': 'form-select'}),
            'chairman_comment': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Comment', 'rows':'4'})
        }


class ProcurementItemForm(forms.ModelForm):
    class Meta:
        model = ProcurementItem
        fields = ['item_name', 'description', 'unit_price', 'quantity_needed', 'reason_for_item_need']
        
        labels = {
            'item_name': 'Name of Item',
            'description': 'Item description',
            'unit_price': 'Item unit price',
            'quantity_needed': 'Number of the item needed',
            'reason_for_item_need': 'Reasons for item need',
        }
        
        widgets = {
            'item_name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Name of Item'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Item description', 'rows':'4'}),
            'unit_price': forms.NumberInput(attrs = {'class': 'form-control'}),
            'quantity_needed': forms.NumberInput(attrs = {'class': 'form-control'}),
            'reason_for_item_need': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Reasons why this item is needed'}),
        }


ProcurementItemFormFormSet = inlineformset_factory(
    ProcurementRequest, ProcurementItem, form=ProcurementItemForm,
    extra=1, can_delete=True, can_delete_extra=True
)