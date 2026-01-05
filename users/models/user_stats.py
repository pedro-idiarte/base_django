from django.db import models
from django.db.models import Sum, Count, Q


class UserStats:
    """
    Helper class to calculate user statistics.
    Not a database model, just for calculations.
    """
    
    @staticmethod
    def get_user_statistics():
        """
        Get all users with their purchase statistics.
        """
        from accounts.models import UserLogin
        from cart.models import Purchase
        
        users = UserLogin.objects.all()
        user_stats = []
        
        for user in users:
            purchases = Purchase.objects.filter(user_email=user.email)
            total_spent = purchases.aggregate(Sum('total_price'))['total_price__sum'] or 0
            purchase_count = purchases.count()
            last_purchase = purchases.last()
            
            user_stats.append({
                'email': user.email,
                'total_spent': total_spent,
                'purchase_count': purchase_count,
                'created_at': user.created_at,
                'last_purchase_date': last_purchase.purchase_date if last_purchase else None,
            })
        
        return user_stats
    
    @staticmethod
    def get_ranking():
        """
        Get user ranking by total spent.
        """
        from accounts.models import UserLogin
        from cart.models import Purchase
        
        users = UserLogin.objects.all()
        ranking = []
        
        for user in users:
            total_spent = Purchase.objects.filter(user_email=user.email).aggregate(
                Sum('total_price')
            )['total_price__sum'] or 0
            
            if total_spent > 0:
                ranking.append({
                    'email': user.email,
                    'total_spent': total_spent,
                })
        
        # Sort by total spent descending
        ranking.sort(key=lambda x: x['total_spent'], reverse=True)
        return ranking
    
    @staticmethod
    def get_user_detail(email):
        """
        Get detailed information about a specific user.
        """
        from accounts.models import UserLogin
        from cart.models import Purchase
        from inventory.models import Product
        
        try:
            user = UserLogin.objects.get(email=email)
        except UserLogin.DoesNotExist:
            return None
        
        purchases = Purchase.objects.filter(user_email=email).select_related('product')
        
        total_spent = purchases.aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Get most purchased products
        products_count = {}
        for purchase in purchases:
            if purchase.product.id not in products_count:
                products_count[purchase.product.id] = {
                    'product': purchase.product,
                    'times_bought': 0,
                    'total_quantity': 0
                }
            products_count[purchase.product.id]['times_bought'] += 1
            products_count[purchase.product.id]['total_quantity'] += purchase.quantity
        
        favorite_products = sorted(
            products_count.values(),
            key=lambda x: x['total_quantity'],
            reverse=True
        )[:5]
        
        return {
            'email': email,
            'created_at': user.created_at,
            'total_spent': total_spent,
            'purchase_count': purchases.count(),
            'purchases': purchases.order_by('-purchase_date'),
            'favorite_products': favorite_products,
        }
    
    @staticmethod
    def get_dashboard_stats():
        """
        Get general dashboard statistics.
        """
        from accounts.models import UserLogin
        from cart.models import Purchase
        
        total_users = UserLogin.objects.count()
        total_purchases = Purchase.objects.count()
        total_revenue = Purchase.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Get unique emails that made purchases
        active_user_emails = Purchase.objects.values_list('user_email', flat=True).distinct()
        active_users = len(active_user_emails)
        
        average_purchase_value = total_revenue / total_purchases if total_purchases > 0 else 0
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_purchases': total_purchases,
            'total_revenue': total_revenue,
            'average_purchase_value': average_purchase_value,
        }
