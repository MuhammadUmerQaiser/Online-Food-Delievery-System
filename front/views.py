from django.shortcuts import render
from django.http import HttpResponse

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
