from django.conf.urls import url

from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/$', views.products, name='products'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.product, name='product'),
    url(r'^products/(?P<pk>[0-9]+)/confirm$', views.confirm, name='confirm'),
    url(r'^products/(?P<pk>[0-9]+)/buy$', views.buy, name='buy'),
    url(r'^thanks$', views.thanks, name='thanks')
]
