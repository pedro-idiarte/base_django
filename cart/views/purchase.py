from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.models import Purchase
from inventory.models import Product
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse


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


@csrf_exempt
def product_api(request, product_id):
    """
    API endpoint for a product supporting GET, PUT and DELETE.

    - GET: return product details as JSON (useful to populate edit forms/modals)
    - PUT: accept JSON body with updatable fields (name, price, stock_quantity, description)
    - DELETE: delete the product
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        data = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price) if hasattr(product, 'price') else None,
            'stock_quantity': product.stock_quantity if hasattr(product, 'stock_quantity') else None,
            'description': getattr(product, 'description', ''),
        }
        return JsonResponse(data)

    if request.method == 'PUT':
        try:
            payload = json.loads(request.body.decode('utf-8') or '{}')
        except Exception:
            return HttpResponseBadRequest('Invalid JSON')

        allowed = ['name', 'price', 'stock_quantity', 'description']
        updated = False
        for field in allowed:
            if field in payload:
                setattr(product, field, payload[field])
                updated = True

        if updated:
            product.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'No valid fields provided'}, status=400)

    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'success': True})

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])


def product_edit(request, product_id):
    """Server-side edit flow using only HTML forms (GET to show form, POST to save)."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'GET':
        return render(request, 'inventory/product_edit.html', {'product': product, 'categories': Product.CATEGORY_CHOICES})

    # POST -> update
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')

        try:
            product.name = name or product.name
            product.description = description or product.description
            if category:
                product.category = category
            if price:
                product.price = float(price)
            if stock_quantity:
                product.stock_quantity = int(stock_quantity)

            product.save()
            messages.success(request, 'Product updated successfully')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

        return redirect('cart:make_purchase')


def product_delete(request, product_id):
    """Server-side delete flow using HTML form (POST)."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted')
    return redirect('cart:make_purchase')
