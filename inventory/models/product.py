from django.db import models


class Product(models.Model):
    """
    Tech/Gaming products inventory model.
    """
    CATEGORY_CHOICES = [
        ('GPU', 'Graphics Card'),
        ('CPU', 'Processor'),
        ('RAM', 'Memory'),
        ('SSD', 'Storage'),
        ('MONITOR', 'Monitor'),
        ('KEYBOARD', 'Keyboard'),
        ('MOUSE', 'Mouse'),
        ('HEADSET', 'Headset'),
        ('MOTHERBOARD', 'Motherboard'),
        ('CASE', 'PC Case'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
