from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AuctionItem, Auction
# Register your models here.

# Register CustomUser with UserAdmin
admin.site.register(CustomUser, UserAdmin)

# Register AuctionItem with default admin
admin.site.register(AuctionItem)

#Register Auction with Admin
admin.site.register(Auction) 