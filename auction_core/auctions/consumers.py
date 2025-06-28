import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Auction, AuctionItem

User = get_user_model()  # This must be kept at the top and used consistently

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.item_id = self.scope['url_route']['kwargs']['item_id']
        self.room_group_name = f'auction_{self.item_id}'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        bid = float(data['bid'])

        # Convert LazyUser to real CustomUser instance
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.send(text_data=json.dumps({
                'error': 'You must be logged in to place a bid.'
            }))
            return

        real_user = await self.get_user(user.id)

        success = await self.update_bid(bid, real_user)
        
        if success:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'auction_bid',
                    'bid': bid,
                    'user': real_user.username
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'error': 'Invalid bid - must be higher than current bid.'
            }))
            
    async def auction_bid(self, event):
        await self.send(text_data=json.dumps({
            'bid': event['bid'],
            'user': event['user']
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
        
    @database_sync_to_async
    def update_bid(self, new_bid, user):
        try:
            item = AuctionItem.objects.get(pk=self.item_id)
            auction = Auction.objects.get(product=item)
            
            if new_bid > float(auction.current_bid):
                auction.current_bid = new_bid
                auction.bidder = user  # ✅ user is now a real CustomUser instance
                auction.save()
                return True
        except (AuctionItem.DoesNotExist, Auction.DoesNotExist):
            pass
        return False
