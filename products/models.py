from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


from django.db.models.deletion import CASCADE
from django.db.models.fields import NullBooleanField
# Create your models here.


# Initializing the Water Products Categiories
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(null=False, blank=False)
    title = models.CharField(max_length=2000, null=False, blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=True, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    delivery_time = models.DateTimeField(default=datetime.now, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.title
# Initializing the Water Categories to be sold


class water_categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Water_Types(models.Model):
    image = models.ImageField(null=False, blank=False)
    title = models.CharField(max_length=2000, null=False, blank=False)
    category = models.ForeignKey(
        water_categories, on_delete=models.CASCADE, default=True, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    delivery_time = models.DateTimeField(default=datetime.now, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.title


# Initializing Service Categories
class water_services_category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Water_Services(models.Model):
    image = models.ImageField(null=False, blank=False)
    title = models.CharField(max_length=2000, null=False, blank=False)
    category = models.ForeignKey(
        water_services_category, on_delete=models.CASCADE, default=True, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_totals(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitems)
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.quantity for item in orderitems)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    waters = models.ForeignKey(
        Water_Types, on_delete=models.SET_NULL, null=True)
    services = models.ForeignKey(
        Water_Services, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price*self.quantity
        return total

    def _str__(self):
        return self.product


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.city)
