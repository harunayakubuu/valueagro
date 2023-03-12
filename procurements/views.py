from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import (
    ProcurementRequestCreateForm, 
    ProcurementItemForm,
    ProcurementItemFormFormSet, 
    MDProcurementRequestApprovalForm,
    ChairmanProcurementRequestApprovalForm,
)

from . models import ProcurementRequest


class ProcurementRequestInline():
    form_class = ProcurementRequestCreateForm
    model = ProcurementRequest
    template_name = "procurements/procurement_request_create_or_update.html"

    def form_valid(self, form):
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
        return redirect('procurements:procurement-requests')
    

    def formset_procurement_items_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        procurement_items = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for procurement_item in procurement_items:
            procurement_item.procurement_request = self.object
            procurement_item.save()


class ProcurementRequestCreate(ProcurementRequestInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProcurementRequestCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'procurement_items': ProcurementItemFormFormSet(prefix='procurement_items'),  
            }
        else:
            return {
                'procurement_items': ProcurementItemFormFormSet(self.request.POST or None, self.request.FILES or None, prefix='procurement_items'),
            }


class ProcurementRequestUpdate(ProcurementRequestInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProcurementRequestUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'procurement_items': ProcurementItemFormFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='procurement_items'),
        }


class ProcurementRequestsList(ListView):
    model = ProcurementRequest
    template_name = "procurements/procurement-requests.html"
    context_object_name = "procurement_requests"


def delete_procurement_item(request, pk):
    try:
        procurement_item = ProcurementItem.objects.get(id=pk)
    except ProcurementItem.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('procurements:update_procurement_request', pk=procurement_item.procurement_request.id)

    procurement_item.delete()
    messages.success(
            request, 'Item deleted successfully'
            )
    return redirect('procurements:update_procurement_request', pk=procurement_item.procurement_request.id)


def procurement_request_details(request, id):
    procurement_request = get_object_or_404(ProcurementRequest, id=id)
    context = {
        'procurement_request': procurement_request
    }
    return render(request, 'procurements/procurement-request-details.html', context)


def procurement_md_approval(request, id):
    procurement_request = get_object_or_404(ProcurementRequest, id=id)
    form = MDProcurementRequestApprovalForm(instance = procurement_request)
    if request.method == 'POST':
        form = MDProcurementRequestApprovalForm(request.POST, instance = procurement_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Saved.")
            return redirect('procurements:procurement-requests')
    context = {
        'procurement_request': procurement_request,
        'form': form

    }
    return render(request, 'procurements/procurement-md-approval.html', context)


def procurement_chairman_approval(request, id):
    procurement_request = get_object_or_404(ProcurementRequest, id=id)
    form = ChairmanProcurementRequestApprovalForm(instance = procurement_request)
    if request.method == 'POST':
        form = ChairmanProcurementRequestApprovalForm(request.POST, instance = procurement_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Saved")
            return redirect('procurements:procurement-requests')
    context = {
        'procurement_request': procurement_request,
        'form': form
    }
    return render(request, 'procurements/procurement-chairman-approval.html', context)


class ProcurementRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = ProcurementRequest
    template_name = 'procurements/procurement-request-delete.html'
    success_url = reverse_lazy('procurements:procurement-requests')