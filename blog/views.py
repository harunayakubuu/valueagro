from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Activity, Category
from .forms import ActivityCreateForm, ActivityEditForm, CategoryCreateForm, CategoryEditForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy


@login_required
def categories(request):
    categories = Activity.objects.order_by('-created_at')
    context = {
        'categories': categories
    }
    return render(request, 'blog/categories.html', context)


@login_required
def category_create(request):
    form = CategoryCreateForm()
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Created.')
            return redirect('blog:categories')
    context = {
        'form': form
    }
    return render(request, 'blog/category-create.html', context)


@login_required
def category_edit(request, id):
    category = Category.objects.get(id = id)
    category_edit_form = CategoryEditForm(instance = category)
    if request.method == 'POST':
        category_edit_form = CategoryEditForm(request.POST, instance = category)
        if category_edit_form.is_valid():
            category_edit_form.save()
            messages.success(request, 'Activity updated successfull.')
            return redirect('blog:categories')
    context = {
        'category_edit_form': category_edit_form,
        'categor': category
    }
    return render(request, 'blog/category-edit.html', context)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'blog/category-delete.html'
    success_url = reverse_lazy('blog:categories')


def public_activities(request):
    activities = Activity.objects.order_by('-created_at').filter(active=True)
    paginator = Paginator(activities, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj
    }
    return render(request, 'blog/public-activities.html', context)


def public_activity_details(request, slug):
    categories = Activity.objects.order_by('title')
    activity = get_object_or_404(Activity, slug=slug)
    related_activities = Activity.objects.order_by('-created_at').filter(category=activity.category).exclude(id=activity.id)[:6]
    context = {
        'activity':activity,
        'related_activities': related_activities,
        'categories': categories
    }
    return render(request, 'blog/public-activity-details.html', context)


@login_required
def all_activities(request):
    activities = Activity.objects.order_by('-created_at')
    context = {
        'activities': activities
    }
    return render(request, 'blog/all-activities.html', context)


@login_required
def activity_create(request):
    form = ActivityCreateForm()
    if request.method == 'POST':
        form = ActivityCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            messages.success(request, 'Activity Created.')
            return redirect('blog:all-activities')
    context = {
        'form': form
    }
    return render(request, 'blog/activity-create.html', context)


@login_required
def activity_edit(request, id):
    activity = Activity.objects.get(id = id)
    update_form = ActivityUpdateForm(instance = activity)
    if request.method == 'POST':
        update_form = PostUpdateForm(request.POST, request.FILES, instance = activity)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Activity updated successfull.')
            return redirect('blog:all-activities')
    context = {
        'update_form': update_form,
        'activity': activity
    }
    return render(request, 'blog/activity-update.html', context)


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'blog/activity-delete.html'
    success_url = reverse_lazy('blog:all-activities')