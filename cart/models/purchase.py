from django.db import models
from inventory.models import Product


class Purchase(models.Model):
    """
    Model to track purchases made by users.
    """
    user_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'purchases'
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f"{self.user_email} - {self.product.name} x{self.quantity}"
