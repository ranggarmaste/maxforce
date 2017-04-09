from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.core.mail import send_mail

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

def buy(request, pk):
    return HttpResponse("Ini harusnya proses form pembelian")

def thanks(request):
    email = request.GET['email']
    template_name = 'shop/thanks.html'
    return render(request, template_name, { 'email': email })

def admin_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('shop:admin_home'))
    template_name = 'admin/login.html'
    next_url = request.GET.get('next')
    if not next_url:
        next_url = '/admin/'
    if request.method == 'GET':
        return render(request, template_name, { 'next_url' : next_url } )
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.GET)
            return redirect(next_url)
        else:
            return render(request, template_name, { 'next_url' : next_url} )

@login_required
def admin_home(request):
    template_name = 'admin/home.html'
    return render(request, template_name)

@login_required
def admin_profile(request):
    template_name = 'admin/profile.html'
    return render(request, template_name)
