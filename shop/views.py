from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.core.mail import send_mail
from instagram.client import InstagramAPI

import requests
import json

fb_access_token = "EAAEApfZASErUBANlOXV3n5UTM57HQsAwX8tkOkRTfOdXV9RZCdqZAYEZAlywoEyI1wGRBYxEV2mhZCLTqdTIoPT0ZB8lOSUQW8pZCv5JX3CuNbJenSb5AqZCFt3NgZCQxdVQmBHKdZBzcrXehNT1d6S1JPfE8PWF9UZAkUZD"
fb_page_id = "1486459264760769"
ig_access_token = "239869696.9761424.59e80d7603964610b7648bbb670443da"
ig_client_secret = "16fd29644c274603bf08a4df517c7a96"

from .models import Product, ProductForm, ProductOrder, ProductOrderForm, Article, ArticleForm, About

def get_facebook():
    info = requests.get('https://graph.facebook.com/v2.8/' + fb_page_id + '?access_token=' + fb_access_token).json()
    data = requests.get('https://graph.facebook.com/v2.8/' + fb_page_id + '/posts?access_token=' + fb_access_token).json()['data']
    for i in range(len(data)):
        post_id = data[i]['id']
        r_post = requests.get('https://graph.facebook.com/v2.8/' + post_id + '/likes?access_token=' + fb_access_token)
        data[i]['likes'] = len(r_post.json()['data'])
    return { 'info' : info, 'data' : data, 'picture' : 'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/17861963_1487341941339168_769261364304292733_n.jpg?oh=f2f6770f70b8acdb995d39a92f5f55c9&oe=59854247'}

def index(request):
    template_name = 'shop/index.html'
    api = InstagramAPI(access_token=ig_access_token, client_secret=ig_client_secret)
    recent_media, next_ = api.user_recent_media(user_id="239869696", count=10)
    facebook_data = get_facebook()
    return render(request, template_name, {'recent_media' : recent_media, 'facebook_data' : facebook_data })

def about(request):
    template_name = 'shop/about.html'
    about = About.objects.all()[0]
    return render(request, template_name, {'about' : about})

def products(request):
    template_name = 'shop/products.html'
    products = Product.objects.all
    return render(request, template_name, { 'products' : products })

def articles(request):
    template_name = 'shop/articles.html'
    articles = Article.objects.all
    return render(request, template_name, { 'articles' : articles})

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

@login_required
def admin_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        form.save()
        return redirect('/admin/')
    # else requestnya GET
    form = ArticleForm()
    template_name = 'admin/adminarticle.html'
    return render(request, template_name, {'form' : form})

@login_required
def admin_product(request):
    template_name = 'admin/adminproduct.html'
    return render(request, template_name)

@login_required
def admin_unpaidorder(request):
    if request.method == "POST":
        pk = request.POST["pk"]
        order = ProductOrder.objects.get(pk=pk)
        order.status = 1
        order.save()
        return redirect('/admin/unpaidorder/')

    template_name = 'admin/adminunpaidorder.html'
    UnpaidOrder = ProductOrder.objects.all().filter(status = 0)
    return render(request, template_name, { 'unpaidorder' : UnpaidOrder})

@login_required
def admin_paidorder(request):
    if request.method == "POST":
        pk = request.POST["pk"]
        order = ProductOrder.objects.get(pk=pk)
        order.status = 2
        order.save()
        return redirect('/admin/paidorder')

    template_name = 'admin/adminpaidorder.html'
    paidorder = ProductOrder.objects.all().filter(status = 1)
    return render(request, template_name, {'paidorder' : paidorder})

@login_required
def admin_historyorder(request):
    template_name = 'admin/adminhistoryorder.html'
    historyorder = ProductOrder.objects.all().filter(status = 2)
    return render(request, template_name, {'historyorder' : historyorder})

@login_required
def admin_add_product(request):
    template_name = 'admin/admin_add_product.html'
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('shop:admin_home'))
        return render(request, template_name, { 'form' : form })

    form = ProductForm(initial={'sold': 10})
    return render(request, template_name, { 'form' : form })
