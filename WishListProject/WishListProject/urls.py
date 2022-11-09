"""WishListProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from WishList.views import login_page, logout_page, list_of_wishlists, own_wishlist, register_page, register_redirect, delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my_list/', own_wishlist),
    path('login/', login_page),
    path('logout', logout_page),
    path('register/', register_page),
    path('register_redirect', register_redirect),
    path('wish/', include('WishList.urls')),
    path('', list_of_wishlists),
]
