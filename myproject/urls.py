
from django.contrib import admin
from django.urls import path, include  # <-- correct include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # <-- include accounts URLs
]
