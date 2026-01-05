from django.shortcuts import render, redirect
from django.contrib import messages
from inventory.models import Product


def product_list(request):
    """
    Display list of all products available for purchase.
    """
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


def product_create(request):
    """
    Create new products - accessible from dashboard.
    Products are saved to the database and visible in admin.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', '')
        price = request.POST.get('price', '')
        stock_quantity = request.POST.get('stock_quantity', '')
        
        # Basic validation
        if not all([name, description, category, price, stock_quantity]):
            messages.error(request, 'All fields are required')
            return render(request, 'inventory/product_create.html', {
                'categories': Product.CATEGORY_CHOICES
            })
        
        try:
            product = Product.objects.create(
                name=name,
                description=description,
                category=category,
                price=float(price),
                stock_quantity=int(stock_quantity)
            )
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('cart:dashboard')
        except ValueError as e:
            messages.error(request, 'Invalid price or stock quantity format')
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
    
    return render(request, 'inventory/product_create.html', {
        'categories': Product.CATEGORY_CHOICES
    })
