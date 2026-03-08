from django.contrib import admin

# Register your models here.
from .models import Product
from category.models import Category

admin.site.register(Product)
admin.site.register(Category)