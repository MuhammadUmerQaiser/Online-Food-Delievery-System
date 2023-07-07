from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('shop/', views.shop, name="shop"),
    path('testimonial/', views.testimonial, name="testimonial"),
    path('payment/', views.payment, name="payment"),
    path('checkout/', views.checkout, name="checkout"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('detail-product/', views.detail_product, name="detail-product"),
    path('auth/', views.authentication, name="authentication"),
]