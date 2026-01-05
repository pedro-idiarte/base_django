from django.contrib import admin
from inventory.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
