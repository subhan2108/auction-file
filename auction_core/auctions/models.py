from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
# Create your models here.

#first day start
class CustomUser(AbstractUser):
    # Add custom fields here if needed
    is_seller = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
class AuctionItem(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auction_items')
    
    def __str__(self):
        return f"{self.name} - {self.status}"
    
    
class Auction(models.Model):
    STATUS_CHOICES = [
        ('active','Active'),
        ('closed','Closed'),
    ]
    
    product = models.OneToOneField('AuctionItem', on_delete=models.CASCADE, related_name='auction')
    current_bid = models.DecimalField( max_digits=10, decimal_places=2, default=0.00)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bids')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    updated_at = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(default=timezone.now() + timedelta(days=1))# ends in 1 hour by default
    
    
    def __str__(self):
        return f"Auction for {self.product.name} -  ₹{self.current_bid}"
    

