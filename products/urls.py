from django.urls import path
from .views import product_list, search_products


urlpatterns = [
    path('', product_list, name="product_list"),
    path('search/', search_products, name="search_products"),
]
