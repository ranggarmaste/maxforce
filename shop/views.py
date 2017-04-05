from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Product, ProductOrder, ProductOrderForm

def index(request):
    template_name = 'shop/index.html'
    return render(request, template_name)

def products(request):
    template_name = 'shop/products.html'
    products = Product.objects.all
    return render(request, template_name, { 'products' : products })

def product(request, pk):
    template_name = 'shop/product.html'
    product = Product.objects.get(pk=pk)
    return render(request, template_name, { 'product' : product })

def confirm(request, pk):
    if request.method == 'POST':
        form = ProductOrderForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('shop:thanks') + '?email=' + form.cleaned_data['email'])
    else:
        product = Product.objects.get(pk=pk)
        form = ProductOrderForm(initial={'product': product})

    return render(request, 'shop/confirm.html', { 'form': form, 'product' : product})

# python manage.py makemigrations
# python manage.py migrate
def buy(request, pk):
    return HttpResponse("Ini harusnya proses form pembelian")

def thanks(request):
    email = request.GET['email']
    template_name = 'shop/thanks.html'
    return render(request, template_name, { 'email': email })
