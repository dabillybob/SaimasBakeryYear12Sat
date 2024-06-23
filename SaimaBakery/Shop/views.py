from django.shortcuts import render


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