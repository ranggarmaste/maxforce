from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    template_name = 'shop/index.html'
    return render(request, template_name)

def products(request):
    template_name = 'shop/products.html'
    return render(request, template_name)

def product(request, pk):
    template_name = 'shop/product.html'
    return render(request, template_name)

def confirm(request, pk):
    template_name = 'shop/confirm.html'
    return render(request, template_name)

def buy(request, pk):
    return HttpResponse("Ini harusnya proses form pembelian")

def thanks(request):
    template_name = 'shop/thanks.html'
    return render(request, template_name)
