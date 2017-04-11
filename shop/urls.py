from django.conf.urls import url

from . import views

app_name = 'shop'
urlpatterns = [
    # USER
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^products/$', views.products, name='products'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.product, name='product'),
    url(r'^products/(?P<pk>[0-9]+)/confirm/$', views.confirm, name='confirm'),
    url(r'^products/(?P<pk>[0-9]+)/buy/$', views.buy, name='buy'),
    url(r'^thanks$', views.thanks, name='thanks'),
    # ADMIN
    url(r'^admin/$', views.admin_home, name='admin_home'),
    url(r'^admin/login/$', views.admin_login, name='admin_login'),
    url(r'^admin/profile/$', views.admin_profile, name='admin_profile'),
    url(r'^admin/product/$', views.admin_product, name='admin_product'),
    url(r'^admin/article/$', views.admin_article, name='admin_article'),
    url(r'^admin/unpaidorder/$', views.admin_unpaidorder, name='admin_unpaidorder'),
    url(r'^admin/paidorder/$', views.admin_article, name='admin_article')
]
