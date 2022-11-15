import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
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
            user = Person.objects.get(name=request.user.username)
            jd = json.JSONDecoder()
            list_of_wishes = jd.decode(str(user.all_ids))
            listw = []
            for wish_id in list_of_wishes:
                obj = get_object_or_404(Object, pk=wish_id)
                listw.append(obj)
            template = loader.get_template('own_wishlist.html')
            context = {
                'list_of_wishes': listw
            }
            return HttpResponse(template.render(context, request))
        
        if request.method == 'POST':
            wish = request.POST.get('wish', '')
            obj, created = Object.objects.get_or_create(name=wish, description='username')
            user = Person.objects.get(name=request.user.username)
            jd = json.JSONDecoder()
            je = json.JSONEncoder()
            list_of_wishes = jd.decode(str(user.all_ids))
            if obj.id not in list_of_wishes:
                list_of_wishes.append(obj.id)
            json_of_wishes = je.encode(list_of_wishes)
            user.all_ids = json_of_wishes
            user.save()
            return redirect('/my_list')
    else:
        return redirect('/login')
    

def list_of_wishlists(request):
    #TODO
    if request.user.is_authenticated:
        if request.method == 'GET':
            listoflists = {}
            listofuserids = []
            for i in range(2):
                rand_person = random.choice(Person.objects.all())
                while rand_person.name == request.user.username or rand_person.name in listofuserids:
                    rand_person = random.choice(Person.objects.all())
                listofuserids.append(rand_person.name)
                jd = json.JSONDecoder()
                list_of_random_wishes = jd.decode(str(rand_person.all_ids))
                list_to_die = []
                for wish_id in list_of_random_wishes:
                    obj = get_object_or_404(Object, pk=wish_id)
                    list_to_die.append(obj)
                listoflists[rand_person.name] = list_to_die
            template = loader.get_template('list_of_wishlists.html')
            context = {
                'list_of_lists': listoflists
            }
            return HttpResponse(template.render(context, request))
        
        if request.method == 'POST':
            wishes = request.POST.getlist('bro')
            user = Person.objects.get(name=request.user.username)
            jd = json.JSONDecoder()
            je = json.JSONEncoder()
            list_of_wishes = jd.decode(str(user.all_ids))
            for wish in wishes:
                obj = Object.objects.get(name=wish, description='username')
                if obj.id not in list_of_wishes:
                    list_of_wishes.append(obj.id)
            json_of_wishes = je.encode(list_of_wishes)
            user.all_ids = json_of_wishes
            user.save()
            return redirect('/')
    else:
        return redirect('/login')
    

def delete(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = Person.objects.get(name=request.user.username)
            jd = json.JSONDecoder()
            je = json.JSONEncoder()
            list_of_wishes = jd.decode(str(user.all_ids))
            list_of_wishes.remove(int(pk))
            json_of_wishes = je.encode(list_of_wishes)
            user.all_ids = json_of_wishes
            user.save()
            return redirect('/my_list')
    else:
        return redirect('/login')
