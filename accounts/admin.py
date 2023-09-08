from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile, Team, CompanyInformation, WarehouseInformation, ShopInformation

User = get_user_model()


class MyAdmin(UserAdmin):
    list_display =('username', 'email', 'first_name', 'middle_name', 'last_name', 'is_active', 'is_superuser', 'last_login')
    search_fields = ('email', 'username', 'phone_number')
    readonly_fields = ('date_joined', 'last_login')
    # readonly_fields = ('id', 'phone_number', 'first_name', 'middle_name', 'last_name', 'date_joined', 'last_login')
    ordering = ('username',)
    list_display_links = ['username',]

    list_filter = (
        ('is_active',)
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal Info'), {'fields': ('first_name', 'middle_name', 'last_name')}),
        (('Contact'), {'fields': ('email', 'phone_number')}),
        (('Permisions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (('User Roles'), {'fields': ('role',)}),
        (('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, MyAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('created_date', 'updated_date')

admin.site.register(Profile, ProfileAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display =('user', 'designation', 'created_date')
    search_fields = ('user',)
    ordering = ('user',)
admin.site.register(Team, TeamAdmin)


class WarehouseInformationInline(admin.StackedInline):
    model = WarehouseInformation
    extra = 0

class ShopInformationInline(admin.StackedInline):
    model = ShopInformation
    extra = 0


class CompanyInformationAdmin(admin.ModelAdmin):
    inlines = [
        WarehouseInformationInline,
        ShopInformationInline
    ]

    list_display =('user', 'company_name', 'company_type', 'state')
    search_fields = ('company_name',)
    ordering = ('state',)
    list_per_page = 20
admin.site.register(CompanyInformation, CompanyInformationAdmin)