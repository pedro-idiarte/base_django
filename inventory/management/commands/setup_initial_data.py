from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from inventory.models import Product


class Command(BaseCommand):
    help = 'Setup initial data for the store'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Admin user created (username: admin, password: admin)'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        # Create sample products
        products_data = [
            {
                'name': 'NVIDIA RTX 4090',
                'description': 'High-end graphics card for gaming and professional work',
                'category': 'GPU',
                'price': 1599.99,
                'stock_quantity': 15
            },
            {
                'name': 'AMD Ryzen 9 7950X',
                'description': '16-core, 32-thread processor for ultimate performance',
                'category': 'CPU',
                'price': 699.99,
                'stock_quantity': 25
            },
            {
                'name': 'Corsair Vengeance RGB 32GB DDR5',
                'description': 'High-speed RGB memory kit',
                'category': 'RAM',
                'price': 179.99,
                'stock_quantity': 40
            },
            {
                'name': 'Samsung 990 PRO 2TB NVMe SSD',
                'description': 'Ultra-fast PCIe 4.0 storage',
                'category': 'SSD',
                'price': 249.99,
                'stock_quantity': 30
            },
            {
                'name': 'LG UltraGear 27" 240Hz',
                'description': 'Gaming monitor with 1ms response time',
                'category': 'MONITOR',
                'price': 449.99,
                'stock_quantity': 20
            },
            {
                'name': 'Razer BlackWidow V3',
                'description': 'Mechanical gaming keyboard with RGB',
                'category': 'KEYBOARD',
                'price': 139.99,
                'stock_quantity': 35
            },
            {
                'name': 'Logitech G Pro X Superlight',
                'description': 'Wireless gaming mouse, ultra-lightweight',
                'category': 'MOUSE',
                'price': 149.99,
                'stock_quantity': 50
            },
            {
                'name': 'SteelSeries Arctis Pro',
                'description': 'Premium gaming headset with Hi-Res audio',
                'category': 'HEADSET',
                'price': 249.99,
                'stock_quantity': 25
            },
            {
                'name': 'ASUS ROG Strix X670E',
                'description': 'High-end AM5 motherboard',
                'category': 'MOTHERBOARD',
                'price': 599.99,
                'stock_quantity': 18
            },
            {
                'name': 'NZXT H710i',
                'description': 'Mid-tower ATX case with RGB and smart features',
                'category': 'CASE',
                'price': 169.99,
                'stock_quantity': 22
            },
        ]
        
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} products'))
        self.stdout.write(self.style.SUCCESS('Setup complete!'))
