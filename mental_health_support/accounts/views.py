from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user:
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('chat')  # Redirect to chat after signup
            else:
                messages.error(request, 'Authentication failed. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors.')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    """Handles user login."""
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('chat')  # Redirect to chat after login
        else:
            messages.error(request, 'Invalid username or password.')
    # else:
    #     form = AuthenticationForm()  # Allow GET requests by rendering the form
    
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    """Handles user logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')  # Redirect to login after logout