
from django.contrib import admin
from django.urls import path, re_path
from . import views

#app_name = 'lists'
urlpatterns = [
    re_path(r'^$', views.home_page, name='home'),
    re_path(r'^lists/(\d+)/$', views.view_list, name='view_list'),
    re_path(r'^lists/new$', views.new_list, name='new_list'),
]