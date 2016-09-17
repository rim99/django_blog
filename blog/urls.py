from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    # '~/blog/'
    url(r'^$', views.index, name='index'),
    # '~/blog/page=2/'
    url(r'^page=(?P<page_num>[0-9]+)/$', views.index, name='index'),
    # '~/blog/blog=HelloWorld/'
    url(r'^blog=(?P<blog>\w+)/$', views.detail, name='detail'),
    # '~/blog/archive/'
    url(r'^archive/$', views.archive, name='archive'),
    # '~/blog/archive/2016/'
    url(r'^archive/year=(?P<year>\d{4})/$', views.archive, name='archive'),
    # '~/blog/archive/2016/page=2'
    url(r'^archive/year=(?P<year>\d{4})/page=(?P<page_num>[0-9]+)/$', views.archive, name='archive'),
    # '~/blog/tag=AdvLinuxProgramming/'
    url(r'^tag=(?P<tag>\w+)/$', views.tag, name='tag'),
    # '~/blog/tag=AdvLinuxProgramming/page=2'
    url(r'^tag=(?P<tag>\w+)/page=(?P<page_num>[0-9]+)/$', views.tag, name='tag'),
 ]
