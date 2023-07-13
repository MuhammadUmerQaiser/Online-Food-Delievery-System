from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
from django.contrib import auth, messages
from django.contrib.auth import login, authenticate
from .models import User, Contact, Order, OrderDetail, Payment
from superUser.models import Dish
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.conf import settings
import stripe
import random
from datetime import date

def index(request):
    dishes = Dish.objects.order_by('-id')[:8]
    return render(request, 'index.html', {'dishes': dishes})

def shop(request):
    dishes = Dish.objects.order_by('-id')
    return render(request, 'shop.html', {'dishes': dishes})

def payment(request):
    order_code = f"{random.randint(100, 999)}-{date.today().strftime('%Y%m%d')}"

    if 'cart' in request.session:
        stripe.api_key = settings.STRIPE_SECRET
        total = 0
        quantity = 0
        data = {}
        for id, details in request.session['cart'].items():
            total += float(details['price']) * int(details['quantity'])
            quantity = details['quantity']
            data[id] = {
                'order_code': order_code,
                'title': details['title'],
                'price': details['price'],
                'quantity': details['quantity'],
            }

            OrderDetail.objects.create(
                order_code=order_code,
                name=details['title'],
                price=details['price'],
                quantity=details['quantity'],
                dish_id=id
            )

        Order.objects.create(
            order_code=order_code,
            address=request.POST['address'],
            note=request.POST['note'],
            total=total,
            user_id=request.session['id'],
            status='Ordered'
        )
        method = 'COD'
        status = 'Pending'
        if request.POST['method'] == 'COD': 
            method = 'COD'
            status = 'Pending'
        else:
            method = 'Stripe'
            status = 'Completed'

        Payment.objects.create(
            order_code=order_code,
            method=method,
            amount=total,
            status=status
        )

        del request.session['cart']

        messages.success(request, "Item buy successfully")
        return redirect('orderSuccess', order_code)

    return redirect('shop')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        description = request.POST['description']

        try:
            contact = Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                description=description
            )
            messages.success(request, "Your query has been submitted successfully!")
            return redirect('contact')

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('contact')
    return render(request, 'contact.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def checkout(request):
    cart = request.session.get('cart', {})
    
    if cart: 
        total = 0
        for details in cart.values():
            price = float(details.get('price', 0))
            quantity = int(details.get('quantity', 0))
            total += price * quantity
        
        return render(request, 'checkout.html', {'total': total})
    else:
        messages.error(request, "Add items in your cart.")
        return redirect('shop')  # Redirect to the shop page with a message

def carts(request):
    return render(request, 'carts.html')

def detail_product(request, slug):
    dish = Dish.objects.filter(slug=slug).first()
    dishes = Dish.objects.order_by('-id')[:4]
    return render(request, 'detail-product.html', {'dish': dish, 'dishes': dishes})

def authentication(request):
    return render(request, 'authentication.html')

def registerUser(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        try:
            if User.objects.filter(email=email).exists():
                raise ValueError('User with this email already exists.')
            encrypted_password = make_password(password)
            
            user = User(name=name, phone=contact, email=email, password=encrypted_password, role=role)
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
                    messages.success(request, 'Logged in successfully!')
                    request.session['name'] = user.name
                    request.session['id'] = user.id
                    request.session['email'] = user.email
                    request.session['contact'] = user.phone
                    request.session['role'] = user.role
                    if user.role == "Admin":
                        return redirect('indexAdmin') 
                    elif user.role == "Owner" :
                        return redirect('indexUser') 
                    else:
                        return redirect('index') 
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
            messages.error(request, 'Please Login')
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




# ADD TO CART
def addToCart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        cart = request.session.get('cart', {})
        product = Dish.objects.filter(id=product_id).first()
        code = 0

        if product:
            if product_id in cart:
                code = 201
                quantity_update = cart[product_id]['quantity'] + int(quantity)

                if quantity_update > product.stock:
                    code = 202
                    return JsonResponse({
                        'status': 'failed',
                        'cartCount': len(cart),
                        'code': 202
                    }, status=202)
                
                cart[product_id]['quantity'] = quantity_update
            else:
                code = 200
                cart[product_id] = {
                    'product_id': product_id,
                    'title': product.name,
                    'quantity': int(quantity),
                    'price': str(product.price),
                    'product_stock': product.stock
                }

            request.session['cart'] = cart

            return JsonResponse({
                'status': 'success',
                'cartCount': len(cart),
                'code': code
            }, status=201 if product_id in cart else 200)

    return JsonResponse({}, status=400)


def updateCart(request):
    if request.method == 'POST':
        if request.POST['product_id'] and request.POST['quantity']:
            product_id = request.POST['product_id']
            quantity = int(request.POST['quantity'])
            cart = request.session.get('cart', {})
            cart[product_id]['quantity'] = quantity
            # cart[product_id] = {'quantity': quantity}
            request.session['cart'] = cart

            total = 0
            for details in cart.values():
                price = float(details.get('price', 0))
                quantity = int(details.get('quantity', 0))
                total += price * quantity

            return JsonResponse({'message': 'Success', 'total': total})


def deleteCart(request):
    if request.method == 'POST' and 'id' in request.POST:
        product_id = request.POST['id']
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

        total = 0
        for details in cart.values():
            price = float(details.get('price', 0))
            quantity = int(details.get('quantity', 0))
            total += price * quantity

        cart_count = len(cart)

        return JsonResponse({'message': 'Success', 'total': total, 'cartCount': cart_count})
    
def orderSuccess(request, code):
    return render(request, 'success.html', {'order_code': code})


def checkOrder(request):
    return render(request, 'check-order.html')

def checkOrderStatus(request):
    if request.method == 'POST':
        order = Order.objects.filter(order_code=request.POST['order_code']).first()

        if order:
            order_details = OrderDetail.objects.filter(order_code=request.POST['order_code'])
            return render(request, 'check-order.html', {'order': order, 'order_details': order_details})
    return render(request, 'check-order.html')

