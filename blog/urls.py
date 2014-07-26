from django.conf.urls import patterns, url
from django.contrib import admin

from blog import views


admin.autodiscover()

urlpatterns = patterns('',
                       
    url(r'^$', views.index, {'ct_name': 'home'},name='index'),
    
    url(r'^category/(?P<ct_name>\w+)/', views.index, name='category'),
    
    url(r'^tag/(?P<ct_name>\w+)/', views.index, name='tag'),
    
    url(r'^article/(?P<article_id>\d+)/$', views.article, name='article'),
    
    url(r'^archive/(?P<published_year>\d{4})/(?P<published_month>\d{1,2})/$', views.archive, name="archive"),
    
    url(r'^about/$', views.about, name='about'),
)
