from django.contrib import admin

from .models import Product
from category.models import Category

admin.site.register(Product)
admin.site.register(Category)