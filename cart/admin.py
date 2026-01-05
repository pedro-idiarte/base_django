from django.contrib import admin
from cart.models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'product', 'quantity', 'total_price', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['user_email', 'product__name']
    readonly_fields = ['purchase_date']

