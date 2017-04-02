from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    template_name = 'shop/index.html'
    return render(request, template_name)
