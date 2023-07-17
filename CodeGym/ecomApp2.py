# This code is adapted from https://github.com/coderaman7/Django-ECommerce-Website

# Import the required modules
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Product, Order, OrderItem, ShippingAddress

# Create your views here.

# Home page view
def home(request):
    # Get all the products from the database
    products = Product.objects.all()
    # Render the home page template with the products
    return render(request, 'home.html', {'products': products})

# Product detail view
def product_detail(request, id):
    # Get the product by id from the database
    product = Product.objects.get(id=id)
    # Render the product detail template with the product
    return render(request, 'product_detail.html', {'product': product})

# Cart view
def cart(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the user's order from the database or create a new one if it doesn't exist
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        # Get the order items from the order
        items = order.orderitem_set.all()
    else:
        # If the user is not authenticated, set the items and order to empty
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    # Render the cart template with the items and order
    return render(request, 'cart.html', {'items': items, 'order': order})

# Checkout view
def checkout(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the user's order from the database or create a new one if it doesn't exist
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        # Get the order items from the order
        items = order.orderitem_set.all()
    else:
        # If the user is not authenticated, set the items and order to empty
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    # Render the checkout template with the items and order
    return render(request, 'checkout.html', {'items': items, 'order': order})

# Update cart view
def update_cart(request):
    # Get the product id and action from the request data
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')
    # Get the user and product from the database
    user = request.user
    product = Product.objects.get(id=product_id)
    # Get or create an order for the user
    order, created = Order.objects.get_or_create(user=user, complete=False)
    # Get or create an order item for the product and order
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    # Perform the action on the order item quantity
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    # Save the order item to the database
    order_item.save()
    # If the quantity is zero, delete the order item from the database
    if order_item.quantity <= 0:
        order_item.delete()
    # Return a success message as a response
    return render(request, 'success.html', {'message': 'Cart updated successfully'})

# Process order view
def process_order(request):
    # Get the transaction id from the request data
    transaction_id = request.POST.get('transaction_id')
    # Get or create an order for the user using the transaction id
    order, created = Order.objects.get_or_create(user=request.user, transaction_id=transaction_id)
    # Set the order as complete and save it to the database
    order.complete = True
    order.save()
    # Create a shipping address for the order using the request data
    ShippingAddress.objects.create(
        user=request.user,
        order=order,
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        state=request.POST.get('state'),
        zipcode=request.POST.get('zipcode')
    )
    # Return a success message as a response
    return render(request, 'success.html', {'message': 'Order processed successfully'}