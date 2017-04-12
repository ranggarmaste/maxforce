from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.core.mail import send_mail
from instagram.client import InstagramAPI
from django.utils.dateparse import parse_datetime

import requests
import json
import sendgrid
import os
from sendgrid.helpers.mail import *

fb_access_token = "EAAEApfZASErUBANlOXV3n5UTM57HQsAwX8tkOkRTfOdXV9RZCdqZAYEZAlywoEyI1wGRBYxEV2mhZCLTqdTIoPT0ZB8lOSUQW8pZCv5JX3CuNbJenSb5AqZCFt3NgZCQxdVQmBHKdZBzcrXehNT1d6S1JPfE8PWF9UZAkUZD"
fb_page_id = "1486459264760769"
ig_access_token = "239869696.9761424.59e80d7603964610b7648bbb670443da"
ig_client_secret = "16fd29644c274603bf08a4df517c7a96"

from .models import Product, ProductForm, ProductOrder, ProductOrderForm, Article, ArticleForm, About, AboutForm

def send_email(order):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("ranggarmaste@gmail.com")
    to_email = Email(order.email)
    subject = '[Maxforce Order #' + str(order.pk) + '] - Payment Confirmation'
    body = 'Dear, ' + order.name + '<br><br>'
    body += 'Here is the detail of your order:<br>'
    body += 'Product: ' + order.product.name + '<br>'
    body += 'Price: ' + str(order.product.price) + '<br>'
    body += 'Delivery Price: ' + str(order.city.delivery_price) + '<br>'
    body += '<b>TOTAL PRICE: ' + str(order.product.price + order.city.delivery_price) + '</b><br><br>'
    body += 'Please pay the given total price to the following bank account:<br>'
    body += 'BNI: 123456789 a/n Sumiah Barbara<br><br>'
    body += 'After you have paid, please reply this email with the attachment of your payment proof<br><br>'
    body += 'Thank you very much<br><br>'
    body += '--Maxforce--<br>'
    content = Content("text/html", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

def parse_date(data):
    for datum in data:
        time = parse_datetime(datum['created_time'])
        datum['created_time'] = str(time.day) + '-' + str(time.month) + '-' + str(time.year) + ', ' + str(time.hour) + ':' + str(time.minute)

def get_facebook():
    info = requests.get('https://graph.facebook.com/v2.8/' + fb_page_id + '?access_token=' + fb_access_token).json()
    data = requests.get('https://graph.facebook.com/v2.8/' + fb_page_id + '/posts?access_token=' + fb_access_token).json()['data']
    parse_date(data)
    for i in range(len(data)):
        post_id = data[i]['id']
        r_post = requests.get('https://graph.facebook.com/v2.8/' + post_id + '/likes?access_token=' + fb_access_token)
        data[i]['likes'] = len(r_post.json()['data'])
    return { 'info' : info, 'data' : data, 'picture' : 'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/17861963_1487341941339168_769261364304292733_n.jpg?oh=f2f6770f70b8acdb995d39a92f5f55c9&oe=59854247'}

def index(request):
    template_name = 'shop/index.html'
    latest_products = Product.objects.all().order_by('-created_at')[:3]
    latest_articles = Article.objects.all().order_by('-created_at')[:3]
    api = InstagramAPI(access_token=ig_access_token, client_secret=ig_client_secret)
    recent_media, next_ = api.user_recent_media(user_id="239869696", count=10)
    facebook_data = get_facebook()
    return render(request, template_name, {'recent_media' : recent_media, 'facebook_data' : facebook_data, 'latest_products' : latest_products, 'latest_articles' : latest_articles })

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
    return render(request, template_name, { 'articles' : articles })

def article(request, pk):
    template_name = 'shop/blog-detail.html'
    article= Article.objects.get(pk=pk)
    return render(request, template_name, { 'article' : article })

def product(request, pk):
    template_name = 'shop/product.html'
    product = Product.objects.get(pk=pk)
    return render(request, template_name, { 'product' : product })

def confirm(request, pk):
    if request.method == 'POST':
        form = ProductOrderForm(request.POST)
        order = form.save()
        send_email(order)
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
def admin_product(request):
    template_name = 'admin/admin_product.html'
    products = Product.objects.all()
    return render(request, template_name, { 'products' : products })

@login_required
def admin_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('shop:admin_product'))

    template_name = 'admin/admin_edit_product.html'
    form = ProductForm(instance=product)
    return render(request, template_name, { 'form' : form, 'product' : product })

@login_required
def admin_delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect(reverse('shop:admin_product'))

@login_required
def admin_add_product(request):
    template_name = 'admin/admin_add_product.html'
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('shop:admin_product'))
        return render(request, template_name, { 'form' : form })

    form = ProductForm(initial={'sold': 10})
    return render(request, template_name, { 'form' : form })

@login_required
def admin_profile(request):
    template_name = 'admin/profile.html'
    profile = About.objects.all()[0]
    print("HEHEHE")
    print(profile.description)
    if request.method == "POST":
        form = AboutForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('shop:about'))
        return render(request, template_name)

    form = AboutForm(instance=profile)
    return render(request, template_name, { 'form' : form, 'about' : about})
