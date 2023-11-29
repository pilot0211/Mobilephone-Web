from django.shortcuts import get_object_or_404, redirect, render
from .models import *
import json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from shop.form import CustomUserForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    product = Product.objects.filter(trending = 1)
    return render(request,'shop/index.html', {'product' : product})

def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user= request.user )
        return render(request,'shop/fav.html', {'fav' : fav})
    else:
        return redirect('/')

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user= request.user )
        return render(request,'shop/cart.html', {'cart' : cart})
    else:
        return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if  request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username = name, password = pwd)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfully!')
                return redirect('/')
            else:
                messages.error('Invalid username or password')
                return redirect('/login')
    return render(request,'shop/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logout successfully!!!')
    return redirect('/')

def register(request):
    form = CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Login Now")
            return redirect('/login')
    return render(request,'shop/register.html', {'form':form})

def collections(request):
    catagory = Catagory.objects.filter(state = 0)
    return render(request,'shop/collections.html',{'catagory': catagory})

def collectionsView(request,name):
    if(Catagory.objects.filter(name=name,state = 0)):
        products=Product.objects.filter(category__name = name)
        return render(request,'shop/products/index.html',{'products': products, 'category_name':name})
    else:
        messages.warning(request, 'No Such Category Found')
        return redirect('collections')

def product_detail(request,cname, pname):
    if(Catagory.objects.filter(name=cname,state = 0)):
        if(Product.objects.filter(name=pname,state = 0)):
            product= Product.objects.filter(name=pname,state = 0).first()
            return render(request,"shop/products/product_detail.html", {'product': product})
        else:
            messages.error(request,'No such catagory found')
            return redirect('collections')
    else:
        messages.error(request,'No such catagory found')
        return redirect('collections')
    
def add_to_cart(request):
    if request.headers.get('X-Request-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            # print(request.user.id)
            product_status = Product.objects.get(pk = product_id)
            if product_status:
                if Cart.objects.filter(user = request.user.id, product_id = product_id):
                    return JsonResponse({'status' : "Product already in cart"}, status = 200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user = request.user, product_id = product_id,product_qty =product_qty )
                        return JsonResponse({'status' : "Product added to cart"}, status = 200)
                    else:
                        return JsonResponse({'status' : "Product is not available"}, status = 200)
            return JsonResponse({'status' : "Product add to cart successfully"}, status = 200)
        else:
            return JsonResponse({'status' : "You need to login to add cart"}, status = 200)
    else:
        return JsonResponse({'status' : "Invalid Access"}, status = 200)
    
def remove_cart(request, cid):
    cartitem = Cart.objects.get(pk = cid)
    cartitem.delete()
    return redirect('/cart')

def remove_fav(request, cid):
    favItem = Favourite.objects.get(pk = cid)
    favItem.delete()
    return redirect('/favviewpage')

def fav_page(request):
    if request.headers.get('X-Request-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(pk = product_id)
            if product_status:
                if Favourite.objects.filter(user = request.user.id, product_id = product_id):
                    return JsonResponse({'status' : "Product already in favourite"}, status = 200)
                else:
                    Favourite.objects.create(user = request.user, product_id = product_id)
                    return JsonResponse({'status' : "Product have added to favourite"}, status = 200)
            
        else:
            return JsonResponse({'status' : "You need to login to add favourite"}, status = 200)
    else:
        return JsonResponse({'status' : "Invalid Access"}, status = 200)
    
