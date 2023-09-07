from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from accounts.views import signup

from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap

sitemaps = {
'products': ProductSitemap,
}



urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('addresses/', include('addresses.urls', namespace='addresses')),
    
    path('value.agro/administration/', admin.site.urls),
    
    path('', include('pages.urls', namespace = 'pages')),
   
    path('blog/', include('blog.urls', namespace = 'blog')),
    path('contacts/', include('contacts.urls', namespace = 'contacts')),
    path('faqs/', include('faqs.urls', namespace = 'faqs')),
    path('invoices/', include('invoices.urls', namespace = 'invoices')),
    path('logistics/', include('logistics.urls', namespace = 'logistics')),
    
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),

    path('newsletters/', include('newsletters.urls', namespace = 'newsletters')),

    path('orders/', include('orders.urls', namespace = 'orders')),
    path('partners/', include('partners.urls', namespace = 'partners')),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done',),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm',),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete',),
    
    path('procurements/', include('procurements.urls', namespace = 'procurements')),
    path('products/', include('products.urls', namespace = 'products')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('signup/', signup, name = 'signup'),
    path('trucks/', include('trucks.urls', namespace = 'trucks')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# handler404='valueagro.views.page_not_found_view'
# handler500='valueagro.views.server_error_view'