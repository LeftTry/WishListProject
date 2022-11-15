from django.urls import path, re_path

from . import views

app_name = 'wishes'

urlpatterns = [
    re_path(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='delete'),
    re_path(r'^delete/adm/(?P<pk>[0-9]+)/$', views.delete_adm, name='delete_obj_adm'),
]
