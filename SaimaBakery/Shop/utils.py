import json
from .models import *


# This file has shortcuts of functions so the code is not as chunky
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except (KeyError, json.JSONDecodeError):
        cart = {}

    print('CART:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
    cartItems = order['get_cart_items']

    for i in cart:
        # Stops page from getting error if something is wrong in cart
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'id': product.id,
                'product': {'id': product.id, 'name': product.name, 'price': product.price,
                            'imageURL': product.imageURL},
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            order['shipping'] = True

        except (Product.DoesNotExist, KeyError):
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        if not isinstance(cookieData, dict):
            cookieData = {'cartItems': 0, 'order': {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True},
                          'items': []}
        cartItems = cookieData.get('cartItems', 0)
        order = cookieData.get('order', {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True})
        items = cookieData.get('items', [])

    return {'cartItems': cartItems, 'order': order, 'items': items}
