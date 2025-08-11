from django.shortcuts import render, redirect
from django.contrib.auth import logout
from item.models import Category, Item

from .forms import SignupForm

def index(request):
    """
    Главная страница: отображает последние 6 непроданных товаров и все категории
    """
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    """
    Страница контактов: просто отображает контактную информацию
    """
    return render(request, 'core/contact.html')


def signup(request):
    """
    Страница регистрации: позволяет новому пользователю зарегистрироваться
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })


def logout_user(request):
    """
    Функция выхода пользователя из системы
    """
    if request.method == 'POST':
        logout(request)
        return redirect("/")
    return render(request, 'core/logout.html')