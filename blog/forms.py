from django import forms
from .models import Activity, Category


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'active')

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Category name'}),
        }

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Category.objects.filter(title__iexact=title)
        if qs.exists():
            self.add_error('title', f"The title, '{title}' already exists.")
        return data


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'active')

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Category name'}),
        }


class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('title', 'category', 'image', 'content', 'active')

        widgets = {
            'content': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Content', 'rows':'5'}),
            'category': forms.Select(attrs = {'class': 'form-select'}),
        }

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Activity.objects.filter(title__iexact=title)
        if qs.exists():
            self.add_error('title', f"The title, '{title}' has already exist.")
        return data


class ActivityEditForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('title', 'category', 'image', 'content', 'active')

        widgets = {
            'content': forms.Textarea(attrs = {'class': 'form-control', 'placeholder':'Content', 'rows':'5'}),
            'category': forms.Select(attrs = {'class': 'form-select'}),
            }