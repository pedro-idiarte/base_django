from django.urls import path
from inventory.views import product_list, product_create

app_name = 'inventory'

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
]
