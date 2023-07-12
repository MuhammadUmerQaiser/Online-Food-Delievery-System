from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'users' 
    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'contacts' 
    def __str__(self):
        return self.name

class OrderStatus(models.TextChoices):
    Ordered = 'Ordered'
    Cooking = 'Cooking'
    Way = 'Way'
    Delievered = 'Delievered'

class Order(models.Model):
    order_code = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    note = models.CharField(null=True, max_length=500)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=OrderStatus.choices, default=OrderStatus.Ordered)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'orders' 
        
    def __str__(self):
       return self.name


class OrderDetail(models.Model):
    order_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.CharField(null=True, max_length=500)
    dish = models.ForeignKey('superUser.Dish', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'order_details' 
        
    def __str__(self):
       return self.name
    
class PaymentStatus(models.TextChoices):
    Pending = 'Pending'
    Completed = 'Completed'

class PaymentMethod(models.TextChoices):
    COD = 'COD'
    Stripe = 'Stripe'

class Payment(models.Model):
    order_code = models.CharField(max_length=255)
    method = models.CharField(max_length=255, choices=PaymentMethod.choices, default=PaymentMethod.Stripe)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=PaymentStatus.choices, default=PaymentStatus.Pending)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'payments' 
        
    def __str__(self):
       return self.name
