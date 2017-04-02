from django.contrib import admin

# Register your models here.
from .models import Article, Product, City, ProductOrder

admin.site.register(Article)
admin.site.register(Product)
admin.site.register(City)
admin.site.register(ProductOrder)
