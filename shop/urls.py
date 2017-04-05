from django.conf.urls import url

from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/$', views.ProductsView.as_view(), name='products'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.ProductView.as_view(), name='product'),
    url(r'^products/(?P<pk>[0-9]+)/confirm$', views.ConfirmView.as_view(), name='confirm'),
    url(r'^products/(?P<pk>[0-9]+)/buy$', views.buy, name='buy'),
    url(r'^thanks$', views.thanks, name='thanks')
]
