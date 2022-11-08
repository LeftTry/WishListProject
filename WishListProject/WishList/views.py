from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Person, Object
import json
from django.template import loader

def login_page(request):
    if request.method == 'GET':
        # если юзер залогинен - редирект на основную стр
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            messages.error(request, 'Заполните все поля!')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неправильный логин или пароль!')
            return redirect('/login')

def register_page(request):
    if request.method == 'GET':
        # если юзер залогинен - редирект на основную стр
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('password_check', '')

        if username == '' or password1 == '' or password2 == '':
            messages.error(request, 'Заполните все поля!')
            return redirect('/register')
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('/register')

        user = User.objects.create_user(username, '', password1)
        person = Person(name=username)
        person.save()
        user.save()
        return redirect('/')
    else:
        messages.error(request, 'Неправильный логин или пароль!')
        return redirect('/register')


def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login')

def register_redirect(request):
    return redirect('/register')

def own_wishlist(request):
    #TODO
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = Person.objects.get(name = request.user.username)
            list_of_wishes = json.JSONDecoder.decode(user.all_ids)
            template = loader.get_template('own_wishlist.html')
            context = {
                'list_of_wishes': list_of_wishes
            }
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/login')

def list_of_wishlists(request):
    #TODO
    if request.user.is_authenticated:
        return render(request, 'list_of_wishlists.html')
    else:
        return redirect('/login')
    