from django.contrib import admin
from .models import Product, SubCatagroy,MainCatagroy, Order
# Register your models here.
admin.site.register(Product)
admin.site.register(SubCatagroy)
admin.site.register(MainCatagroy)
admin.site.register( Order)