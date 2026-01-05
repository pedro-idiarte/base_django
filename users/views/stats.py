from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from users.models.user_stats import UserStats


def user_list(request):
    """
    Display list of all users with their statistics.
    """
    user_statistics = UserStats.get_user_statistics()
    
    context = {
        'user_statistics': user_statistics,
    }
    
    return render(request, 'users/user_list.html', context)


def user_ranking(request):
    """
    Display ranking of users by total spent.
    """
    ranking = UserStats.get_ranking()
    
    context = {
        'ranking': ranking,
    }
    
    return render(request, 'users/user_ranking.html', context)


def user_detail(request, email):
    """
    Display detailed information about a specific user.
    """
    user_detail = UserStats.get_user_detail(email)
    
    if not user_detail:
        messages.error(request, f'User {email} not found')
        return render(request, 'users/user_not_found.html')
    
    context = {
        'user': user_detail,
    }
    
    return render(request, 'users/user_detail.html', context)


def dashboard(request):
    """
    Display admin dashboard with general statistics.
    """
    stats = UserStats.get_dashboard_stats()
    
    # Calculate conversion rate
    conversion_rate = 0
    if stats['total_users'] > 0:
        conversion_rate = (stats['active_users'] / stats['total_users']) * 100
    
    context = {
        'stats': stats,
        'conversion_rate': round(conversion_rate, 1),
    }
    
    return render(request, 'users/dashboard.html', context)
