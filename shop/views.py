from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Product

def index(request):
    template_name = 'shop/index.html'
    return render(request, template_name)

class ProductsView(generic.ListView):
    template_name = 'shop/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all

class ProductView(generic.DetailView):
    template_name = 'shop/product.html'
    model = Product

class ConfirmView(generic.DetailView):
    template_name = 'shop/confirm.html'
    model = Product

def buy(request, pk):
    return HttpResponse("Ini harusnya proses form pembelian")

def thanks(request):
    template_name = 'shop/thanks.html'
    return render(request, template_name)
