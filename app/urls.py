"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^case/$', views.case, name='case'),
    url(r'^customer/$', views.customer, name='customer'),
    # url(r'^detail/(?P<slug>\w+)/$', views.detail, name='detail'),
    # url(r'^detail/(?P<slug>)/$', views.case_detail, name='case_detail'),
    url(r'^caseDetail/(?P<case_slug>\w+)/$', views.case_detail, name='case_detail'),
    url(r'^customerDetail/(?P<customer_slug>\w+)/$', views.customer_detail, name='customer_detail'),
    # url(r'^about/$', TemplateView.as_view(template_name='app/about.html'), name='about'),
    # url(r'^detail/(?P<category>\w+)/$', views.ArticleOptions, name='options'),
    # url(r'^type/(?P<type>\w+)/$', views.ArticleTypes, name='type'),
    # url(r'^detail/(?P<category>\w+)/(?P<type>\w+)/$', views.ArticleList, name='list'),
    # url(r'^detail/(?P<category>\w+)/(?P<type>\w+)/(?P<pk>\d+)/$', views.detail, name='detail'),
    # url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentView, name='comment'),
    # url(r'^article/like/add/$', views.Post_like, name='like'),
    # url(r'^about/$', views.AboutView, name='about'),
    # url(r'^about/(?P<category>\w+)/$', views.AboutList, name='aboutlist'),
    # url(r'^about/(?P<category>\w+)/(?P<article_id>\d+)/$', views.AboutDetail, name='aboutdetail'),

]
