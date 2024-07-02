from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
class MainCatagroy(models.Model):
      name=models.CharField(max_length=70)
      def __str__(self):
        return self.name

class SubCatagroy(models.Model):
    main_cat=models.ForeignKey(MainCatagroy,on_delete=models.CASCADE)
    name=models.CharField(max_length=70)
    photo=models.ImageField(upload_to='catphoto',null=True,blank=True)
    def __str__(self):
        return self.name
# Create your models here.
class Product(models.Model):

    name=models.CharField(max_length=60)
    sub_cat = models.ForeignKey(SubCatagroy, on_delete=models.CASCADE,null=True)
    photo=models.ImageField(upload_to='prophoto',null=True,blank=True)
    decription=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='Products'
class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('user','product')
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}-{self.product.name}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=timezone.now() + timedelta(days=3))  # Delivery date is 3 days after the order date
    status = models.CharField(max_length=20, default='Pending')  # Status of the order (Pending, Completed, Rejected)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')