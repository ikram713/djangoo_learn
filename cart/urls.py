from django.urls import path
from .views import add_to_cart  # import the view

urlpatterns = [
    path('add/', add_to_cart, name='add_to_cart'),
]
