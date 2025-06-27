from django.urls import path
from .views import signup_view, login_view, logout_view
from .views import (
    AuctionItemCreateView,
    AuctionItemDetailView,
    AuctionItemListView,
    AuctionItemDeleteView,
    AuctionItemUpdateView,
)

urlpatterns = [
    path('', AuctionItemListView.as_view(), name='item_list'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    path('item/<int:pk>/edit/', AuctionItemUpdateView.as_view(), name='item-update'),
    path('item/new/', AuctionItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/delete/', AuctionItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/', AuctionItemDetailView.as_view(), name='item-detail'),
]
