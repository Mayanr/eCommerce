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
    for item in request.session['cart_']:
        if item['id'] == int(prod_id):
            item['quant'] += int(request.POST['quant'])
            request.session.modified = True
            return redirect('/cart_contents')
    
    request.session['cart_'].append({'id':int(prod_id), 'quant': int(request.POST['quant']), 'ppu': float(request.POST['price']), 'total': 0.00})

    print(request.session['cart_'])
    request.session.modified = True
    return redirect('/cart_contents')


def shopping_cart(request):
    if 'cart_' not in request.session:
        request.session['cart_'] = []
    print(request.session['cart_'])

    item_ids_in_cart = []
    cart_count = 0
    cart_sumTotal_cost = 0
    allPrices = []
    tax = 0
    shipping = 5.00 
    sub_total = 0
    for x in request.session['cart_']:
        cart_count += x['quant']
        item_ids_in_cart.append(str(x['id']))
        x['total'] = x['quant']*x['ppu']
        cart_sumTotal_cost += x['total']
        price_list=[]
        pricingArr = []
        pricingArr.append({'id': x['id'], 'price_list': price_list})
        for i in range(1,21):
            price_list.append(i*x['ppu'])
        allPrices.append(pricingArr)
        tax = cart_sumTotal_cost * 0.06
        sub_total = tax + shipping + cart_sumTotal_cost

    context= {
        'cart_count' : cart_count,
        'cart_sumTotal_cost': cart_sumTotal_cost,
        'price_list' : allPrices,
        'cart_contents' : request.session['cart_'],
        'prods' : Prod.objects.filter(id__in=item_ids_in_cart),
        'tax' : tax,
        'shipping_cost' : shipping,
        'sub_total' : sub_total
    }
    return render(request, 'online_shopping/cart.html', context)


def edit_cart(request, prod_id):
    for item in request.session['cart_']:
        if item['id'] == int(prod_id):
            item['quant'] = int(request.POST['new_quant'])
            request.session.modified = True
            return redirect('/cart_contents')

def remove_from_cart(request, prod_id):
    for item in request.session['cart_']:
        if item['id'] == int(prod_id):
            request.session['cart_'].remove(item)
            request.session.modified = True
            return redirect('/cart_contents')

def checkout(request):
    cart_count = 0
    item_ids_in_cart = []
    cart_sumTotal_cost = 0
    tax = 0
    shipping = 5.00 
    sub_total = 0
    for x in request.session['cart_']:
        cart_count += x['quant']
        item_ids_in_cart.append(str(x['id']))
        x['total'] = x['quant']*x['ppu']
        cart_sumTotal_cost += x['total']
        tax = cart_sumTotal_cost * 0.06
        sub_total = tax + shipping + cart_sumTotal_cost

    
    context = {
        'cart_count' : cart_count,
        'prods' : Prod.objects.filter(id__in=item_ids_in_cart),
        'cart_contents' : request.session['cart_'],
        'cart_sumTotal_cost': cart_sumTotal_cost,
        'tax' : tax,
        'shipping_cost' : shipping,
        'sub_total' : sub_total
    }
    return render(request, 'online_shopping/checkout.html', context)

def empty_cart(request):
    del request.session['cart_']
    return redirect('/cart_contents')


def process_order(request):
    errors = Order.objects.basic_validator(request.POST)
    print(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print('entries no good')
    else:
        email = request.POST['email']

        bill_fname = request.POST['bill_fname']
        bill_lname = request.POST['bill_lname']
        bill_address = request.POST['bill_address']
        bill_address2 = request.POST['bill_address2']
        bill_city = request.POST['bill_city']
        bill_state = request.POST['bill_state']
        bill_zip = request.POST['bill_zip']

        ship_fname = request.POST['ship_fname']
        ship_lname = request.POST['ship_lname']
        ship_address = request.POST['ship_address']
        ship_address2 = request.POST['ship_address2']
        ship_city = request.POST['ship_city']
        ship_state = request.POST['ship_state']
        ship_zip = request.POST['ship_zip']

        total_cost = request.POST['total_cost']
        status = Status.objects.get(id=1)
        # add_to_cat = Category.objects.get(id = c)
        # new_cat = Category.objects.create(title = c)
        new_order = Order.objects.create(email = email, b_fname = bill_fname, b_lname = bill_lname, b_address = bill_address, b_address2 = bill_address2, b_city = bill_city, b_state = bill_state, b_zip = bill_zip, sh_fname = ship_fname, sh_lname = ship_lname, sh_address = ship_address, sh_address2 = ship_address2, sh_city = ship_city, sh_state = ship_state, sh_zip = ship_zip, total_cost = total_cost, status = status)
        for key, value in request.POST.lists():
            print(key, value)
            if key=='prod':
                prods = value
            if key=='quant':
                quant = value
            if key=='cost':
                cost = value
        # new_order = Order.objects.get(id=1)
        for p,q,c in zip(prods,quant,cost):
            # print("p is qual to ", p, "and q is" , q)
            ordered_prod = Prod.objects.get(id=p)
            Order_Item.objects.create(includes_prod = ordered_prod, quant = q, cost =c, belongs_to_shopper = new_order)

        return redirect('/confirmation')
    return redirect('/checkout')


def confirmation(request):
    # del request.session['cart_']
    request.session['cart_'] = []
    return render(request, 'online_shopping/confirmation.html')

# --------------------admin routes---------------------------


def admin_login(request):
    return render(request, 'online_shopping/admin.html')  


# password NEVER stored in the views file! Generally password (hashed) is stored securely in the database. The following lines of code are here solely to set up a single log-in for this demo site. The 'verify_admin' view is to demonstrate hasing and validating passwords, securely.

#this creds Dictionary is holding the log-in credentials- this would normally be referenced in a db. 
creds = {'id': 1, 'user_email': "test@outlook.com", 'psswrd': bcrypt.hashpw('demo_login'.encode(), bcrypt.gensalt()) }

#here we'll verify the e-mail belongs to an existing user, and subsequently check whether the password matches the hashed password attached to the user.
def verify_admin(request):
    if request.POST['admin_email']== creds['user_email']:
        if bcrypt.checkpw(request.POST['admin_pw'].encode(), creds['psswrd']):
            request.session['logged_in'] = creds['id']
            return redirect('/dashboard/orders')
        else: 
            messages.error(request, 'Invalid Login Credentials')
            return redirect('/admin')
    else:
        messages.error(request, 'Invalid Login Credentials')
        return redirect('/admin')


def admin_logout(request):
    if 'logged_in' in request.session:
        del request.session['logged_in']
        messages.error(request, 'Successful log out. Thanks for visiting, see you next time!')
        return redirect('/admin')
    else:
        messages.error(request, 'You must be logged in to access this page. Please log in below or contact your site adminstrator to obtain the credentials.')
        return redirect('/admin')


def dashboard_orders(request):
    if 'logged_in' in request.session:
        context = {
            'orders' : Order.objects.all(),
        }
        return render(request, 'online_shopping/dashboard.html', context)
    else:
        messages.error(request, 'You must be logged in to access this page. Please log in below or contact your site adminstrator to obtain the credentials.')
        return redirect('/admin')


def dashboard_prods(request):
    if 'logged_in' in request.session:
        context = {
            'products' : Prod.objects.order_by('-updated_at'),
            'categories' : Category.objects.all(),
            # 'order_by_name' : Prod.objects.order_by('name')
        }
        return render(request, 'online_shopping/dashboard_prods.html', context)
    else:
        messages.error(request, 'You must be logged in to access this page. Please log in below or contact your site adminstrator to obtain the credentials.')
        return redirect('/admin')


def orders_show(request, order_id):
    if 'logged_in' in request.session:
        this_order = Order.objects.get(id=order_id)
        total = (float(this_order.total_cost) - 5)/1.06
        tax = float(this_order.total_cost) - total - 5
        context= {
            'selected_order' : this_order,
            'order_details' : Order_Item.objects.filter(belongs_to_shopper=order_id),
            'tax' : tax,
            'total' : total
        }
        return render(request, "online_shopping/orders_show.html", context)
    else:
        messages.error(request, 'You must be logged in to access this page. Please log in below or contact your site adminstrator to obtain the credentials.')
        return redirect('/admin')


def add_prod(request):
    if 'logged_in' in request.session:
        # errors = Prod.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #         print('entries no good')
        #     return redirect('/dashboard/prods')
        # else:
        n = request.POST['name']
        d = request.POST['desc']
        p = request.POST['unit_price']
        c = request.POST['category']
        img = request.POST['main_pic']
        count = request.POST['inventory_count']
        add_to_cat = Category.objects.get(id = c)
        Prod.objects.create(name = n, desc = d, price = p, cat = add_to_cat, count = count, main_img = img)
        return redirect('/dashboard/prods')
    else:
        messages.error(request, 'You must be logged in to access this page. Please log in below or contact your site adminstrator to obtain the credentials.')
        return redirect('/admin')


def delete_prod(request, prod_id):
    if 'logged_in' in request.session:
        Prod.objects.filter(id= prod_id).delete()
        return redirect('/dashboard/prods')
    else:
        messages.error(request, 'You must be logged in to access this page. Please log in below or contact your site adminstrator to obtain the credentials.')
        return redirect('/admin')


def update_prod(request):
    if 'logged_in' in request.session:
        editing_prod = Prod.objects.get(id=request.POST['prod_id'])
        # errors = Prod.objects.basic_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #         print('entries no good')
    #     return redirect('/dashboard/prods')
    # else:
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
    else:
        messages.error(request, 'You must be logged in to access this page. Please log in below or contact your site adminstrator to obtain the credentials.')
        return redirect('/admin')

def update_order_status(request, order_id):
    if 'logged_in' in request.session:
        updated_order = Order.objects.get(id=order_id)
        print(updated_order.status.id)
        updated_order.status_id = request.POST['status']
        updated_order.save()
        print(updated_order.status_id)
        return redirect('/dashboard/orders')
    else:
        messages.error(request, 'You must be logged in to access this page. Please log in below or contact your site adminstrator to obtain the credentials.')
        return redirect('/admin')
    