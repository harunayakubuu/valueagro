import random
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from .token import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from addresses.models import DeliveryAddress
from .models import Profile, CompanyInformation, WarehouseInformation, ShopInformation

#Import for Formtools
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .forms import (
    CompanyInformationForm,
    WarehouseInformationForm,
    ShopInformationForm,

    UserRegistrationForm,
    StaffUserCreateForm,
    UserAccountEditForm,
    UserProfileEditForm,
    UserRoleEditForm,
)
from .models import Account
from orders.views import user_orders

User = get_user_model()


@login_required
def dashboard(request):
    total_customers = User.objects.filter(role = 'CUSTOMER')
    total_agents = User.objects.filter(role = 'AGENT')
    # orders_delivered = Order.objects.filter(order_status = 'Delivered')
    orders = user_orders(request)
        
    context = {
        'total_customers': total_customers,
        'total_agents': total_agents,
        # 'orders_delivered': orders_delivered
        'orders': orders
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    my_delivery_addresses = DeliveryAddress.objects.filter(user=request.user.profile)
    context = {
        "my_delivery_addresses": my_delivery_addresses
    }
    return render(request, 'accounts/profile.html', context)


def show_warehouse_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('warehouse_available')

class CustomerKYCWizardView(LoginRequiredMixin, SessionWizardView):
    form_list = [CompanyInformationForm, WarehouseInformationForm, ShopInformationForm]
    template_name = 'accounts/customer_kyc_form.html'

    condition_dict = {'1': show_warehouse_form}

    file_storage = FileSystemStorage(location = os.path.join(settings.MEDIA_ROOT, 'photos'))

    def done(self, form_list, **kwargs):
        company_form = form_list[0]
        if company_form.cleaned_data.get('warehouse_available'):
            company = company_form.save(commit = False)
            company.user = self.request.user
            company.save()

            warehouse_form = form_list[1]

            warehouse = warehouse_form.save(commit=False)
            warehouse.company = company
            warehouse.save()
        else:
            company = company_form.save(commit = False)
            company.user = self.request.user
            company.save()
        
        shop = form_list[-1].save(commit = False)
        shop.company = company
        shop.save()

        return HttpResponse('Data saved.')
        # return HttpResponseRedirect('/accounts/data-saved/')
    
@login_required
def agro_dealers(request):
    agro_dealers = CompanyInformation.objects.all()
    context = {
        'agro_dealers': agro_dealers
    }
    return render(request, 'accounts/agro-dealers.html', context)


@login_required
def agro_dealer_details(request, id):
    dealer = get_object_or_404(CompanyInformation, id = id)
    context = {
        'dealer': dealer
    }
    return render(request, 'accounts/agro-dealer-details.html', context)
# @login_required
# def customer_kyc_form(request):
#     form = CompanyInformationForm()
#     if request.method == "POST":
#         form = CompanyInformationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form_instance = form.save(commit = False)
#             # form.save(commit = False)
#             form_instance.user = request.user
#             form_instance.save()
#             messages.success(request, "Data saved")
#             return redirect('accounts:customer-kyc-form')
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/customer-kyc-form.html', context)



@login_required
def users(request):
    users = User.objects.order_by('-date_joined').all()
    context = {
        'users': users,
    }
    return render(request, 'accounts/users.html', context)




email = EmailMessage(
'Hello',
'Body goes here',
'from@example.com',
['to1@example.com', 'to2@example.com'],
['bcc@example.com'],
reply_to=['another@example.com'],
headers={'Message-ID': 'foo'},
)

# Staff User Creation Form
@login_required
def staff_user_create(request):
    form = StaffUserCreateForm()
    if request.method == 'POST':
        form = StaffUserCreateForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save(commit = False)
            pswd = f'{random.randint(0, 1000000000)}'
            user.set_password(pswd)
            user.save()

            subject = "Staff User Registration"
            message = f'You have been added as a staff of Value Agro. Please use the credentials below to log in and change your password. Username: {user.username}, Email: {user.email}, and Password: {pswd}'
            email = EmailMessage(
                subject = subject,
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipients = [user.email,],
                reply_to=[settings.EMAIL_HOST_USER]
            )
            email.send()
            messages.success(request, f'User, {user.username} has successfully been created.')
            return redirect('accounts:staff-user-create')
        else:
           messages.error(request, 'Invalid form entries. Check and try again.') 

    context = {
        'form': form,
    }
    return render(request, 'accounts/staff-user-create.html', context)


# This page is viewed by the Admin HR
@login_required
def user_details(request, username):
    user = get_object_or_404(User, username = username)
    context = {
        'user': user
    }
    return render(request, 'accounts/user-details.html', context)


@login_required
def user_role_edit(request, id):
    user = get_object_or_404(User, id = id)
    form = UserRoleEditForm(instance=user)
    if request.method == 'POST':
        form = UserRoleEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('accounts:users')
        else:
           messages.error(request, 'Check the form and try again.') 

    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'accounts/user-role-edit.html', context)


@login_required
def user_account_edit(request):
    form = UserAccountEditForm(instance=request.user)
    user_profile_form = UserProfileEditForm(instance = request.user.profile)

    if request.method == 'POST':
        form = UserAccountEditForm(request.POST, request.FILES or None, instance=request.user)
        user_profile_form = UserProfileEditForm(request.POST, request.FILES or None, instance=request.user.profile)
        if form.is_valid() and user_profile_form.is_valid():
            form.save()
            user_profile_form.save()
            messages.success(request, 'Changes saved.')
            return redirect('accounts:user-account-edit')
        else:
           messages.error(request, 'Check the form and try again.') 

    context = {
        'form': form,
        'user_profile_form': user_profile_form
    }
    return render(request, 'accounts/user-account-edit.html', context)


@login_required
def account_delete_confirm(request):
    user = Account.objects.get(username = request.user.username)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('accounts:account-delete-confirm')


@login_required
def account_delete(request):
    return render(request, 'registration/account-delete-confirm.html')


# Public Customer Registration Form
def signup(request):
    form = UserRegistrationForm()
    # if request.user.is_authenticated:
    #     return redirect('/')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():       
            user = form.save(commit = False)
            
            user.is_active = False
            user.role = 'CUSTOMER'

            user.save()
            
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject = subject, message = message)
            # return HttpResponse("Registration successful. Activation sent to your email account")
            # messages.success(request, 'We have sent an activation link to your email')
            return redirect('/accounts/account-success')
        else:
            messages.error(request, 'Check and correct the error below.')
    
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


def account_success(request):
    return render(request, 'registration/account-success.html')


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("accounts:dashboard")
    else:
        return render(request, 'accounts/account-activation-invalid.html')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/user-delete.html'
    success_url = reverse_lazy('accounts:users')