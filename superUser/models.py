from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to='category/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'categories' 
        
    def __str__(self):
        return self.name
    

class FoodType(models.Model):
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'food_types' 
        
    def __str__(self):
        return self.name
    

class Dish(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to='dish/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('front.User', on_delete=models.CASCADE)
    food_type = models.ForeignKey('FoodType', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'dishes' 
        
    def __str__(self):
        return self.name
