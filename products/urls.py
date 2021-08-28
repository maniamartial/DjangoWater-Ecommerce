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
    path('update/', views.updateItem, name='update'),
    path('payment', views.paymentmethods, name='payment'),
    path('processOrder/', views.processOrder, name='processOrder'),
    # ADMIN
    path('addProduct', views.addProduct, name='addProduct'),
    path('modifyAllProduct', views.showProduct, name='modifyAllProduct'),
    path('updateProduct/<int:pk>', views.updateProduct, name='updateProduct'),
    path('deleteProduct/<int:pk>', views.deleteProduct, name='deleteProduct'),
    path('modifySingleProduct/<int:pk>',
         views.modifySingleProduct, name='modifySingleProduct'),
    path('addCategory',
         views.addCategory, name='addCategory'),
]
