from django.conf.urls import patterns, url
from django.contrib import admin

from blog import views


admin.autodiscover()

urlpatterns = patterns('',
                       
    url(r'^$', views.index, name="index"),
    url(r'^article/$', views.article, name="article"),
    url(r'^archive/(?P<published_year>\d{4})/(?P<published_month>\d{1,2})/$', views.archive, name="archive"),
)
