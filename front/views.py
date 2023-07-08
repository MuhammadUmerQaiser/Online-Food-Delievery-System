from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
from django.contrib import auth, messages
from django.contrib.auth import login, authenticate
from .models import User
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop.html')

def payment(request):
    return render(request, 'payment.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def checkout(request):
    return render(request, 'checkout.html')

def detail_product(request):
    return render(request, 'detail-product.html')

def authentication(request):
    return render(request, 'authentication.html')

def registerUser(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        email = request.POST['email']
        password = request.POST['password']
        try:
            if User.objects.filter(email=email).exists():
                raise ValueError('User with this email already exists.')
            encrypted_password = make_password(password)
            
            user = User(name=name, phone=contact, email=email, password=encrypted_password, role="User")
            user.save()
            
            messages.success(request, 'User registered successfully!')
            return redirect('registerUser')
        
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('registerUser')
    return render(request, 'authentication.html')

def loginUser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).first()
                if check_password(password, user.password):
                    request.session['name'] = user.name
                    request.session['id'] = user.id
                    request.session['email'] = user.email
                    request.session['contact'] = user.phone
                    request.session['role'] = user.role
                    messages.success(request, 'Logged in successfully!')
                    return redirect('authentication') 
                else:
                    messages.error(request,"Invalid password.")
                    return redirect('authentication')
            else:
                messages.error(request,"Invalid email.")
                return redirect('authentication')
        
        except User.DoesNotExist:
            raise ValueError('Invalid email or password')
    
    return render(request, 'authentication.html')


# checks for authentciation
def authenticated_only(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not 'name' in request.session:
            return redirect('loginUser')  # Redirect to your login page
        return view_func(request, *args, **kwargs)
    return wrapped_view


def logoutUser(request):
    del request.session['name']
    del request.session['id']
    del request.session['email']
    del request.session['contact']
    del request.session['role']
    return redirect('index')  