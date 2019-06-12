from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import*
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    if 'cart_' not in request.session:
        request.session['cart_'] = []
    else:
        request.session['cart_']

    cart_count = 0
    for x in request.session['cart_']:
        cart_count += x['quant']
    
    context = {
        'categories' : Category.objects.order_by('title'),
        'cart_count' : cart_count
    }
    return render(request, "online_shopping/index.html", context)


def prods_category(request, cat_id):
    cart_count = 0
    for x in request.session['cart_']:
        cart_count += x['quant']

    context = {
        'categories' : Category.objects.all().distinct(),
        'selected_cat' : Category.objects.get(id=cat_id).title,
        'prods_in_cat' : Prod.objects.filter(cat = cat_id).values,
        'cart_count' : cart_count
    }
    return render(request, "online_shopping/products_category.html", context)


def prods_show(request, prod_id):
    thisProd = Prod.objects.get(id=prod_id)
    pricingArr = []
    for i in range(1,21):
        pricingArr.append(i*thisProd.price)

    cart_count = 0
    for x in request.session['cart_']:
        cart_count += x['quant']

    context= {
        'selected_prod' : Prod.objects.get(id=prod_id),
        'price_list' : pricingArr,
        'cart_count' : cart_count
    }
    return render(request, "online_shopping/prods_show.html", context)


def add_to_cart(request, prod_id):
    if 'cart_' not in request.session:
        request.session['cart_'] = []
    print(request.session['cart_'])

    for item in request.session['cart_']:
        if item['id'] == int(prod_id):
            item['quant'] += int(request.POST['quant'])
            request.session.modified = True
            return redirect('/cart_contents')
    
    request.session['cart_'].append({'id':int(prod_id), 'quant': int(request.POST['quant']), 'ppu': float(request.POST['price']), 'total': 0.00})

    # request.session['cart_']['total']=request.session['cart_']['ppu']*request.session['cart_']['quant']

    print(request.session['cart_'])
    request.session.modified = True
    return redirect('/cart_contents')


def shopping_cart(request):
    if 'cart_' not in request.session:
        request.session['cart_'] = []
    print(request.session['cart_'])

    item_ids_in_cart = []
    cart_count = 0
    for x in request.session['cart_']:
        cart_count += x['quant']
        item_ids_in_cart.append(str(x['id']))
        x['total'] = x['quant']*x['ppu']
    

    context= {
        'cart_count' : cart_count,
        'cart_contents' : request.session['cart_'],
        'prods' : Prod.objects.filter(id__in=item_ids_in_cart),
        'allProds' : Prod.objects.all()
    }
    return render(request, 'online_shopping/cart.html', context)

def empty_cart(request):
    # if 'cart_' not in request.session:
    #     request.session['cart_'] = []
    # request.session['cart'] = []
    del request.session['cart_']
    # request.session.clear()
    return redirect('/cart_contents')

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
        'products' : Prod.objects.order_by('name'),
        'categories' : Category.objects.all(),
        # 'order_by_name' : Prod.objects.order_by('name')
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

def delete_prod(request, prod_id):
    Prod.objects.filter(id= prod_id).delete()
    return redirect('/dashboard/prods')

def update_prod(request):
    editing_prod = Prod.objects.get(id=request.POST['prod_id'])
    print(editing_prod.name)
    errors = Prod.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print('entries no good')
        return redirect('/dashboard/prods')
    else:
        editing_prod.name = request.POST['name']
        editing_prod.desc = request.POST['desc']
        editing_prod.price = request.POST['unit_price']
        c = request.POST['category']
        add_to_cat = Category.objects.get(id = c)
        editing_prod.cat = add_to_cat
        editing_prod.main_img = request.POST['main_pic']
        editing_prod.count = request.POST['inventory_count']
        editing_prod.save()
    return redirect('/dashboard/prods')

    