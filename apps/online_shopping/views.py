from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import*
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from PIL import Image



def index(request):
    context = {
        'categories' : Category.objects.order_by('title')
    }
    return render(request, "online_shopping/index.html", context)

def prods_category(request, cat_id):
    context = {
        'categories' : Category.objects.all().distinct(),
        'selected_cat' : Category.objects.get(id=cat_id).title,
        'prods_in_cat' : Prod.objects.filter(cat = cat_id).values
    }
    return render(request, "online_shopping/products_category.html", context)

def prods_show(request, prod_id):
    context= {
         'selected_prod' : Prod.objects.get(id=prod_id),
    }
    return render(request, "online_shopping/prods_show.html", context)

def add_to_cart(request, prod_id):
    return redirect('/carts')

def shopping_cart(request):
    return render(request, 'online_shopping/cart.html')

def process_payment(request):
    pass

def confirmation(request):
    pass
    # return render([HTML CONFIRMATION PAGE])

# --------------------admin routes---------------------------

def admin_login(request):
    return render(request, 'online_shopping/admin.html')

def verify_admin(request):
    return redirect('/dashboard/orders')

def dashboard_orders(request):
    context = {
        'orders' : Order.objects.all(),

    }
    return render(request, 'online_shopping/dashboard.html', context)

def dashboard_prods(request):
    context = {
        'products' : Prod.objects.all(),
        'categories' : Category.objects.order_by('title')
    }
    return render(request, 'online_shopping/dashboard_prods.html', context)

def orders_show(request, order_id):
    # context= {
    #      'selected_order' : Order.objects.get(id=order_id),
    # }
    return render(request, "online_shopping/orders_show.html")

def add_prod(request):
    errors = Prod.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print('entries no good')
        return redirect('/dashboard/prods')
    else:
        n = request.POST['name']
        d = request.POST['desc']
        p = request.POST['unit_price']
        c = request.POST['category']
        img = request.POST['main_pic']
        count = request.POST['inventory_count']
        add_to_cat = Category.objects.get(id = c)
        # new_cat = Category.objects.create(title = c)
        Prod.objects.create(name = n, desc = d, price = p, cat = add_to_cat, count = count, main_img = img)
    return redirect('/dashboard/prods')
    