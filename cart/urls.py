from django.urls import path
from cart.views.purchase import dashboard, make_purchase, product_api, product_edit, product_delete

app_name = 'cart'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('purchase/', make_purchase, name='make_purchase'),
    path('product/<int:product_id>/', product_api, name='product_api'),
    path('product/<int:product_id>/edit/', product_edit, name='product_edit'),
    path('product/<int:product_id>/delete/', product_delete, name='product_delete'),
]
