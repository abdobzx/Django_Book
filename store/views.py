from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from .models import Product

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

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
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')  # Replace 'home' with your desired homepage URL
        else:
            error_message = "Invalid username or password."
            return render(request, 'accounts/login.html', {'error_message': error_message})
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login.html') 

from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = Customer(user=user)
            customer.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

from django.shortcuts import render
from .models import Product

def search_view(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query) if query else []
    context = {'products': products, 'query': query}
    return render(request, 'store/search.html', context)

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Retrieve the product using the provided product_id

    context = {'product': product}
    return render(request, 'store/product_details.html', context)
    # Render the product details page template with the product object as context


from django.shortcuts import render

def contact(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Do something with the form data
        # For example, you can save it to a database or send an email

        # Render a success page or redirect to a different URL
        return render(request, 'success.html')

    # If the request method is GET, simply render the contact form
    return render(request, 'store/contact.html')
	


def product_list(request):
    # Fetch all products from the database
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'store/product_list.html', context)


def privacy_policy(request):
	return render(request,'store/privacy policy.html')


def payment_methoth(request):
	return render(request, 'store/payment methoth.html')


def Our_services(request):
	return render(request, 'store/Our_services.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Account, Order

@login_required
def account_info(request):
    user = request.user
    
    # Retrieve the user's account
    account = Account.objects.get(user=user)
    
    # Retrieve the user's orders
    orders = Order.objects.filter(account=account)
    
    context = {
        'account': account,
        'orders': orders,
		
    }
    
    return render(request, 'store/account_info.html', context)
