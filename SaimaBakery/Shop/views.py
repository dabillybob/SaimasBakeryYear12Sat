from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData

#rendering the pages so it shows up on application
#cart items is to calculate total number of items in cart
def Shop(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'Shop/Shop.html', context)

def Cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context  = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'Shop/Cart.html', context)



def Checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context  = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'Shop/Checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    if orderItem.quantity <= 0:
        orderItem.delete()
    else:
        orderItem.save()

    return JsonResponse('Item was updated', safe=False)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transaction_id = datetime.datetime.now().timestamp()

            if request.user.is_authenticated:
                # Handle authenticated user
                customer = request.user.customer
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
                total = float(data['form']['total'])
                order.transaction_id = transaction_id

                if total == order.get_cart_total:
                    order.complete = True
                order.save()

                if 'shipping' in data:
                    ShippingAddress.objects.create(
                        customer=customer,
                        order=order,
                        address=data['shipping']['address'],
                        city=data['shipping']['city'],
                        state=data['shipping']['state'],
                        postcode=data['shipping']['postcode']
                    )

                return JsonResponse({'status': 'success', 'message': 'Payment complete'})

            else:
                # Handle non-authenticated user
                print('User is not logged in')
                print('COOKIES:', request.COOKIES)

                name = data['form']['name']
                email = data['form']['email']

                cookieData = cookieCart(request)
                items = cookieData['items']

                customer, created = Customer.objects.get_or_create(email=email)
                customer.name = name
                customer.save()

                order = Order.objects.create(customer=customer, complete=False)

                for item in items:
                    product = Product.objects.get(id=item['id'])
                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        quantity=item['quantity'],
                    )

                total = float(data['form']['total'])
                order.transaction_id = transaction_id

                if total == order.get_cart_total:
                    order.complete = True
                order.save()

                if 'shipping' in data:
                    ShippingAddress.objects.create(
                        customer=customer,
                        order=order,
                        address=data['shipping']['address'],
                        city=data['shipping']['city'],
                        state=data['shipping']['state'],
                        postcode=data['shipping']['postcode']
                    )

                return JsonResponse({'status': 'success', 'message': 'Payment submitted..'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {e}'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
