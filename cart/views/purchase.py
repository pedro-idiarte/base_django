from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.models import Purchase
from inventory.models import Product


def dashboard(request):
    """
    Dashboard view showing:
    - User's purchase history
    - Links to create products and make purchases
    """
    user_email = request.session.get('user_email')
    
    if not user_email:
        messages.warning(request, 'Please login to view dashboard')
        return redirect('accounts:login')
    
    # Get user's purchases
    purchases = Purchase.objects.filter(user_email=user_email)
    
    context = {
        'user_email': user_email,
        'purchases': purchases,
    }
    
    return render(request, 'cart/dashboard.html', context)


def make_purchase(request):
    """
    View to make a purchase.
    Displays available products and allows user to buy them.
    """
    user_email = request.session.get('user_email')
    
    if not user_email:
        messages.warning(request, 'Please login to make a purchase')
        return redirect('accounts:login')
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        
        try:
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)
            
            if quantity <= 0:
                messages.error(request, 'Quantity must be greater than 0')
                return redirect('cart:make_purchase')
            
            if product.stock_quantity < quantity:
                messages.error(request, f'Not enough stock. Available: {product.stock_quantity}')
                return redirect('cart:make_purchase')
            
            # Calculate total price
            total_price = product.price * quantity
            
            # Create purchase
            purchase = Purchase.objects.create(
                user_email=user_email,
                product=product,
                quantity=quantity,
                total_price=total_price
            )
            
            # Update stock
            product.stock_quantity -= quantity
            product.save()
            
            messages.success(request, f'Purchase successful! Bought {quantity}x {product.name} for ${total_price}')
            return redirect('cart:dashboard')
            
        except ValueError:
            messages.error(request, 'Invalid quantity')
        except Exception as e:
            messages.error(request, f'Error processing purchase: {str(e)}')
    
    # Get all available products
    products = Product.objects.filter(stock_quantity__gt=0)
    
    return render(request, 'cart/make_purchase.html', {'products': products})
