from django.urls import path
from cart.views import dashboard, make_purchase

app_name = 'cart'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('purchase/', make_purchase, name='make_purchase'),
]
