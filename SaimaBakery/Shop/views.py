from django.shortcuts import render
from .models import *

def store(request):
    products = Product.objects.all
    context = {'products':products}
    return render(request, 'Shop/Shop.html')

#rendering the pages so it shows up on application
def Shop(request):
    context  = {}
    return render(request, 'Shop/Shop.html', context)

def Cart(request):
    context  = {}
    return render(request, 'Shop/Cart.html', context)

def Checkout(request):
    context  = {}
    return render(request, 'Shop/Checkout.html', context)