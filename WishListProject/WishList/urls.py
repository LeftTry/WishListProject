from django.urls import path, re_path

from . import views

app_name = 'wishes'

urlpatterns = [
    re_path(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='delete'),
    path(r'^delete/adm/<str:name>/<int:pk>', views.delete_adm, name='delete_obj_adm'),
]
