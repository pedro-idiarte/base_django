from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import UserLogin


def login_view(request):
    """
    Simple login view with basic validation:
    - Email must contain @gmail
    - Password must be longer than 3 characters
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if '@gmail' not in email.lower():
            messages.error(request, 'Email must be a Gmail address (@gmail)')
            return render(request, 'accounts/login.html')
        
        if len(password) <= 3:
            messages.error(request, 'Password must be longer than 3 characters')
            return render(request, 'accounts/login.html')
        
        user_login, created = UserLogin.objects.get_or_create(
            email=email,
            defaults={'password': password}
        )
        
        request.session['user_email'] = email
        
        if created:
            messages.success(request, f'Welcome! Account created for {email}')
        else:
            messages.success(request, f'Welcome back, {email}!')
        
        return redirect('cart:dashboard')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    Simple logout view that clears the session.
    """
    if 'user_email' in request.session:
        del request.session['user_email']
    messages.success(request, 'Logged out successfully')
    return redirect('accounts:login')
