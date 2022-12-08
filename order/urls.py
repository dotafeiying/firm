from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^commit$', views.order_commit, name='order_commit'),
    url(r'^pay$', views.order_pay, name='order_pay'),
    url(r'^test/$', views.test, name='test'),
    # url(r'^case/$', views.case, name='case'),
    # url(r'^customer/$', views.customer, name='customer'),
    # url(r'^detail/(?P<slug>\w+)/$', views.detail, name='detail'),
    # url(r'^detail/(?P<slug>)/$', views.case_detail, name='case_detail'),
    url(r'^goods_detail/(?P<goods_slug>\w+)/$', views.goods_detail, name='goods_detail'),
    # url(r'^customerDetail/(?P<customer_slug>\w+)/$', views.customer_detail, name='customer_detail'),
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