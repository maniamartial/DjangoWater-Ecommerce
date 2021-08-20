from os import name
from django.urls import path
from .import views
urlpatterns = [

    path('waters', views.waterSamples, name='waters'),
    path('services', views.waterServices, name="services"),
    path('products', views.waterProducts, name='products'),
    path('product/<int:pk>/', views.productDetail, name='product'),
    path('fun', views.funAndGames, name='fun'),
    path('help', views.help, name='help'),
    path('about_us', views.aboutUs, name='about_us'),
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('cart', views.userCart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('allproducts', views.AllProducts, name='all-products'),
    path('update/', views.updateItem, name='update')
]
