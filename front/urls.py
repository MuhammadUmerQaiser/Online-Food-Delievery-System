from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('shop/', views.shop, name="shop"),
    path('testimonial/', views.testimonial, name="testimonial"),
    path('payment/', views.authenticated_only(views.payment), name="payment"),
    path('order/success/<str:code>/', views.orderSuccess, name="orderSuccess"),
    path('checkout/', views.authenticated_only(views.checkout), name="checkout"),
    path('carts/', views.carts, name="carts"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('check-order/', views.checkOrder, name="checkOrder"),
    path('check-order-status/', views.checkOrderStatus, name="checkOrderStatus"),
    # path('contact/', views.authenticated_only(views.contact), name="contact"),
    path('detail-product/<slug:slug>/', views.detail_product, name="detail-product"),
    path('auth/', views.authentication, name="authentication"),
    path('register/', views.registerUser, name="registerUser"),
    path('login/', views.loginUser, name="loginUser"),
    path('logout/', views.logoutUser, name="logoutUser"),
    path('add-to-cart/', views.addToCart, name="addToCart"),
    path('update-cart/', views.updateCart, name="updateCart"),
    path('delete-cart/', views.deleteCart, name="deleteCart"),
]