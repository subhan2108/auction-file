from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AuctionItem, Auction

@receiver(post_save, sender=AuctionItem)
def create_auction(sender, instance, created, **kwargs):
    if created:
        Auction.objects.create(product=instance)