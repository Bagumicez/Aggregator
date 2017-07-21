from django.conf.urls import url
from . import views

app_name = 'parse'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sort_view$', views.sort_view, name='sort_view'),
    url(r'^load/(?P<source>[a-zA-z]+)$', views.load, name='load'),
    url(r'^show/(?P<source>[a-zA-z]+)$', views.show_result, name='show'),
]
