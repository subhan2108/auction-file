from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import AuctionItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auctions/signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('item-list')
    else:
        form = AuthenticationForm()
    return render(request, 'auctions/login.html', {'form':form})


def logout_view(request):
    logout(request)
    return redirect('login')




# List all products
class AuctionItemListView(ListView):
    model = AuctionItem
    template_name = 'auctions/item_list.html'
    context_object_name = 'items'
    
# View one product    
class AuctionItemDetailView(DetailView):
    model = AuctionItem
    template_name = 'auctions/item_detail.html'
    
# Create new product
class AuctionItemCreateView(LoginRequiredMixin, CreateView):
    model = AuctionItem
    fields = ['name', 'description', 'starting_price', 'status', 'photo']
    template_name = 'auctions/item_form.html'
    success_url = reverse_lazy('item_list')
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    
    # Update product
class AuctionItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AuctionItem
    fields = ['name', 'description', 'starting_price', 'status', 'photo']
    template_name = 'auctions/item_form.html'
    success_url = reverse_lazy('item_list')
    
    def test_func(self):
        item = self.get_object()
        return item.seller == self.request.user
    
    
    #delete product
class AuctionItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AuctionItem
    template_name = 'auctions/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')
    
    def test_func(self):
        item = self.get_object()
        return item.seller == self.request.user