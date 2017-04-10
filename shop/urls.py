from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

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
    url(r'^admin/profile/$', views.admin_profile, name='admin_profile')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
