from products.forms import CategoryForm, ProductForm
from django.core import paginator
from products.models import Category, Order, OrderItem, Product, ShippingAddress
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.db.models import Prefetch
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
import json

import datetime

# Directs the user to teh homepage


def home(request):
    return render(request, "products/index.html")


# It shows different waters sold
def waterSamples(request):
    categories = Category.objects.filter(name__startswith="Waters")

    page_num = request.GET.get("page")
    paginator = Paginator(categories, 3)
    try:
        categories = paginator.page(page_num)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categores = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {' get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']

    waters = Product.objects.all()

    context = {
        'categories': categories, 'waters': waters, 'cartitems': cartitems
    }

    return render(request, "products/waterSamples.html", context)


# Different Water Services
def waterServices(request):
    categories = Category.objects.filter(
        name__startswith="Services")
    page_num = request.GET.get("page")
    paginator = Paginator(categories, 3)
    try:
        categories = paginator.page(page_num)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categores = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {' get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']

    waterservices = Product.objects.all()

    context = {
        'categories': categories, 'waterservicess': waterservices, 'cartitems': cartitems
    }
    return render(request, "products/waterServicesPage.html", context)

# Different water Products


def waterProducts(request):
    categories = categories = Category.objects.filter(
        name__startswith="Products").order_by('name')
    page_num = request.GET.get("page")
    paginator = Paginator(categories, 3)
    try:
        categories = paginator.page(page_num)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {' get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']

    waters = Product.objects.all()
    context = {
        'categories': categories, 'waters': waters, 'cartitems': cartitems
    }
    return render(request, "products/WaterProductPage.html", context)


# Help page
def help(request):
    return render(request, 'products/help.html')

# About us page


def aboutUs(request):
    return render(request, 'products/aboutus.html')


def funAndGames(request):
    return render(request, 'products/waterfunpage.html')


def productDetail(request, pk):
    eachProduct = Product.objects.get(id=pk)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {' get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']

    context = {
        'cartitems': cartitems,
        'eachProduct': eachProduct,

    }
    return render(request, 'products/singleProduct.html', context)

# Search functionalities


def search(request):

    if request.method == "POST":
        search = request.POST['q']
        categories = Category.objects.filter(name__contains=search)
        '''Water_Categories = water_categories.objects.filter(
            name__contains=search)
        Service_categories = water_services_category.objects.filter(
            name__contains=search)'''
        product = Product.objects.filter(title__contains=search)
    # q = request.POST['q']
    # data = Category.objects.filter(name__icontains=q).order_by('-id')
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartitems = order.get_cart_items
        else:
            items = []
            order = {' get_cart_total': 0, 'get_cart_items': 0}
            cartitems = order['get_cart_items']
        context = {
            'search': search,
            'categories': categories,
            'product': product,
            'cartitems': cartitems
        }
        return render(request, "products/search.html", context)
    else:
        return render(request, "products/search.html", {})


@ login_required
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()

        cartitems = order.get_cart_items
    else:
        items = []
        order = {' get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'products/checkout.html', context)


# Customers cart
def userCart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {' get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'products/cart.html', context)


def updateItem(request):
    print('Data: is this', request.body)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action', action)
    print('productId:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    '''waters = Water_Types.objects.get(id=productId)
    services = Water_Services.objects.get(id=productId),'''
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderitem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'remove':
        orderitem.quantity = (orderitem.quantity-1)
        print("Removed")

    elif action == 'remove-completely':
        orderitem.quantity = (orderitem.quantity == 0)
        print("Removed from cart")

    elif action == 'add':
        orderitem.quantity = (orderitem.quantity+1)
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('It was added', safe=False)


# Integrating the site with Mpesa and paypal payment methods3
def paymentmethods(request):
    return render(request, "products/payment.html")


# Last recap of Order processing
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = order.get_cart_totals
        order.transaction_id = transaction_id

        if total == order.get_cart_totals:
            order.complete = True
        order.save()

        if order.shipping == True:
            print("Wrong")
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                firstname=data['shipping']['firstname'],
                lastname=data['shipping']['lastname'],
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                zipcode=data['shipping']['zipcode']
            )
    else:
        print("User doesn't exist")
    print('Data:', request.body)
    return JsonResponse('Payment Submitted', safe=False)


# Dealing with Managers-Admin-
# Create, Update and Delete Categories, subcategories and Products
def showProduct(request):
    allproducts = Product.objects.all()
    context = {
        'allproducts': allproducts

    }
    return render(request, 'products/Admin/modifyAllProducts.html', context)


# Manager add product
def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('modifyAllProduct')
        else:
            form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'products/Admin/addProduct.html', context)


# Manager updating Product
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('modifyAllProduct')
        else:
            form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'products/Admin/updateProduct.html', context)


# Manager deleting product
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('modifyAllProduct')


# Manager accessing details of products
def modifySingleProduct(request, pk):
    eachProduct = Product.objects.get(id=pk)
    context = {
        'eachProduct': eachProduct}
    return render(request, 'products/Admin/modifySingleProduct.html', context)


# Managers adding a category
def addCategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('modifyAllProduct')
        else:
            form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'products/Admin/addCategory.html', context)
