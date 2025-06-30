import asyncio
import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Auction, AuctionItem

User = get_user_model()

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.item_id = self.scope['url_route']['kwargs']['item_id']
        self.room_group_name = f'auction_{self.item_id}'
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.user_group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send current auction status immediately
        status = await self.get_auction_status()
        await self.send(text_data=json.dumps({'status': status}))

        self.check_status_task = asyncio.create_task(self.check_auction_status())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)
        self.check_status_task.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        bid = float(data.get('bid', 0))
        user = self.user

        if not user.is_authenticated:
            await self.send(text_data=json.dumps({
                'error': 'You must be logged in to place a bid.'
            }))
            return

        real_user = await self.get_user(user.id)
        success, outbid_user_id = await self.update_bid(bid, real_user)

        if success:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'auction_bid',
                    'bid': bid,
                    'user': real_user.username,
                }
            )

            # Notify the previous highest bidder
            if outbid_user_id and outbid_user_id != real_user.id:
                await self.channel_layer.group_send(
                    f"user_{outbid_user_id}",
                    {
                        'type': 'outbid_notification',
                        'message': f"You've been outbid on item #{self.item_id}."
                    }
                )
        else:
            await self.send(text_data=json.dumps({
                'error': 'Invalid bid - must be higher than current bid or auction is closed.'
            }))

    async def auction_bid(self, event):
        await self.send(text_data=json.dumps({
            'bid': event['bid'],
            'user': event['user']
        }))

    async def auction_status_update(self, event):
        await self.send(text_data=json.dumps({
            'status': event['status']
        }))

    async def outbid_notification(self, event):
        await self.send(text_data=json.dumps({
            'notification': event['message']
        }))

    async def check_auction_status(self):
        last_status = None
        while True:
            current_status = await self.get_auction_status()
            if current_status != last_status:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'auction_status_update',
                        'status': current_status
                    }
                )
                last_status = current_status

            if current_status == "closed":
                break
            await asyncio.sleep(5)

    @database_sync_to_async
    def get_auction_status(self):
        try:
            auction = Auction.objects.get(product_id=self.item_id)
            if auction.end_time and auction.end_time <= timezone.now():
                if auction.status != 'closed':
                    auction.status = 'closed'
                    auction.save()
                return "closed"
            return "ongoing"
        except Auction.DoesNotExist:
            return "unknown"

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def update_bid(self, new_bid, user):
        try:
            auction = Auction.objects.get(product_id=self.item_id)
            if auction.status == 'closed':
                return False, None
            if new_bid > float(auction.current_bid):
                outbid_user_id = auction.bidder.id if auction.bidder else None
                auction.current_bid = new_bid
                auction.bidder = user
                auction.save()
                return True, outbid_user_id
        except (Auction.DoesNotExist, AuctionItem.DoesNotExist):
            pass
        return False, None
