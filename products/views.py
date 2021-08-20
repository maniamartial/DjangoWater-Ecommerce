from django.core import paginator
from products.models import Category, Order, OrderItem, Product, Water_Services, Water_Types, water_categories, water_services_category
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.db.models import Prefetch
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
import json


def home(request):
    return render(request, "products/index.html")


# Differet water types
def waterSamples(request):
    categories = water_categories.objects.prefetch_related(Prefetch(
        'water_types_set',
        queryset=Water_Types.objects.filter(
            is_published=True).order_by('-price')
    ))

    page_num = request.GET.get("page")
    paginator = Paginator(categories, 3)
    try:
        categories = paginator.page(page_num)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categores = paginator.page(paginator.num_pages)
    context = {
        'categories': categories
    }
    return render(request, "products/waterSamples.html", context)


# Different Water Services
def waterServices(request):
    categories = water_services_category.objects.prefetch_related(Prefetch(
        'water_services_set',
        queryset=Water_Services.objects.filter(
            is_published=True).order_by('-price')
    ))
    page_num = request.GET.get("page")
    paginator = Paginator(categories, 3)
    try:
        categories = paginator.page(page_num)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categores = paginator.page(paginator.num_pages)
    context = {
        'categories': categories
    }
    return render(request, "products/waterServicesPage.html", context)

# Different water Products


def waterProducts(request):
    categories = Category.objects.prefetch_related(Prefetch(
        'product_set',
        queryset=Product.objects.filter(is_published=True).order_by('-price')
    ))
    page_num = request.GET.get("page")
    paginator = Paginator(categories, 3)
    try:
        categories = paginator.page(page_num)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categores = paginator.page(paginator.num_pages)
    context = {
        'categories': categories
    }
    return render(request, "products/WaterProductPage.html", context)


@login_required
def help(request):
    return render(request, 'products/help.html')


@login_required
def aboutUs(request):
    return render(request, 'products/aboutus.html')


def funAndGames(request):
    return render(request, 'products/waterfunpage.html')


def productDetail(request, pk):
    eachProduct = Product.objects.get(id=pk)
    context = {
        'eachProduct': eachProduct}
    return render(request, 'products/singleProduct.html', context)

# Search functionalities


def search(request):
    if request.method == "POST":
        search = request.POST['q']
        categories = Category.objects.filter(name__contains=search)
        Water_Categories = water_categories.objects.filter(
            name__contains=search)
        Service_categories = water_services_category.objects.filter(
            name__contains=search)

    #q = request.POST['q']
    #data = Category.objects.filter(name__icontains=q).order_by('-id')
        return render(request, "products/search.html", {'search': search,
                                                        'categories': categories,
                                                        'Water_Categories': Water_Categories,
                                                        'Service_categories': Service_categories})
    else:
        return render(request, "products/search.html", {})


@login_required
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


def AllProducts(request):
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

    allproducts = Product.objects.all()
    context = {'allproducts': allproducts,  'cartitems': cartitems}
    return render(request, "products/AllProducts.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action', action)
    print('Product:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer)

    orderitem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity+1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity-1)
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('It was added', safe=False)
