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
