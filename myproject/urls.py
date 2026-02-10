
from django.contrib import admin
from django.urls import path, include  # <-- correct include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # <-- include accounts URLs
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/cart/', include('cart.urls')),  # <-- include cart endpoints
]
