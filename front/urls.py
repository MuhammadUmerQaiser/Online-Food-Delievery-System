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
    # path('contact/', views.authenticated_only(views.contact), name="contact"),
    path('detail-product/<slug:slug>/', views.detail_product, name="detail-product"),
    path('auth/', views.authentication, name="authentication"),
    path('register/', views.registerUser, name="registerUser"),
    path('login/', views.loginUser, name="loginUser"),
    path('logout/', views.logoutUser, name="logoutUser"),
    path('add-to-cart/', views.addToCart, name="addToCart"),
]