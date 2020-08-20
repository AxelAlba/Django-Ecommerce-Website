from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import * 


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    
    products = Product.objects.all()
    context = {'products':products, 'cartItems' : cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated: #if the user is logged in
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #creating an object if it does not exist, else only query
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems' : cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request): #same with cart
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems' : cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body) # we objectify the json string sent by cart.js
    productId = data['productId'] #dictonaries
    action = data['action']

    print('Action: ', action)
    print('productId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer = customer, 
        complete = False)
    orderItem, created = OrderItem.objects.get_or_create(
        order = order, 
        product = product
    )
    # to not create a new item for the same order
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    # if the quantity is 0, delete it
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe = False)