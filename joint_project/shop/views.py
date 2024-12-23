from django.shortcuts import render, get_object_or_404
from .models import Shop, Category

# Create your views here.

def index(requests):
    shop = Shop.objects.all()
    context = {'title': 'Главная', 'shops': shop}
    return render(requests, 'shop/index.html', context)

def detain_goods(requests, pk):
    shop = get_object_or_404(Shop, pk=pk)
    context = {'title': shop.name, 'shop': shop}
    return render(requests, 'shop/detail.html', context)

def category(requests):
    cats = Category.objects.all()
    context = {'title': 'Категории', 'cats': cats}
    return render(requests, 'shop/category.html', context)
