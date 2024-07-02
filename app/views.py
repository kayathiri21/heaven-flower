from datetime import timedelta
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import MainCatagroy,SubCatagroy,Product, Wishlist,Cart,Order ,OrderItem
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
def home(request):
    main=MainCatagroy.objects.all()
    selected_subcategory_id = request.GET.get('subcatagory_id')
    show_login_message = request.GET.get('show_login_message', False)
    if selected_subcategory_id:
        # If a subcategory is selected, filter products based on that subcategory
        subcatagory = SubCatagroy.objects.get(pk=selected_subcategory_id)
        products = Product.objects.filter(sub_cat=subcatagory)
    else:
        # If no subcategory is selected, show all products
        products = Product.objects.all()

    return render(request, "./app/index.html", {'mcat': main, 'products': products,'show_login_message': show_login_message})



def product_details(request,product_id):
     product=get_object_or_404(Product,pk=product_id)
     similar_products=Product.objects.filter(Q(sub_cat=product.sub_cat )& ~Q(id=product.id))[:3]
     return render(request,"./app/product_detail.html",{"product":product,"similar_products":similar_products})
# whishlist start
@login_required
def add_wishlist(request,product_id):
     if not request.user.is_authenticated:
        return redirect(f'/?show_login_message=True')
     product=get_object_or_404(Product,pk=product_id)
     wishlist_item,created= Wishlist.objects.get_or_create(user=request.user,product=product)
     if not created:
          wishlist_item.delete()
          messages.success(request,'product removed from whishlist successfully')
     else:
          messages.success(request,'product added from whishlist successfully')
     return redirect('wishlist')
@login_required
def view_wishlist(request):
     if not request.user.is_authenticated:
        return redirect(f'/?show_login_message=True')
     wishcount=0
     if request.user.is_authenticated:
          wishcount=Wishlist.objects.filter(user=request.user).count()
     wishitems=Wishlist.objects.filter(user=request.user)    
     return render(request,"./app/wishlist.html",{'wishlist_item': wishitems,"wishlist_count": wishcount})

# whishlist end






def about(request):
    return render(request,'./app/about.html')

def add_to_cart(request, product_id):
     if not request.user.is_authenticated:
        return redirect(f'/?show_login_message=True')
     if request.method=='POST':
          product = get_object_or_404(Product, pk=product_id)
          quantity=int(request.POST.get('quantity',1))
          if quantity<1:
               return HttpResponseBadRequest('Invalid quantity')
          cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
          if not created:
               cart_item.quantity += quantity
               cart_item.save()
          else:
               cart_item.quantity = quantity
               cart_item.save()
          return redirect('cart')
     else:
          return HttpResponseBadRequest("Invalid request method")
#     product = get_object_or_404(Product, pk=product_id)
#     cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

# #     cart_item.quantity+=1
# #     cart_item.save()
       

#     return redirect('cart')


@login_required
def view_cart(request):
    if not request.user.is_authenticated:
        return redirect(f'/?show_login_message=True')
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        action = request.POST.get('action')
        for item in cart_items:
            if action == f'decrease_{item.id}' and item.quantity > 1:
                item.quantity -= 1
            elif action == f'increase_{item.id}':
                item.quantity += 1
            item.save()
        return redirect('cart')

    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    return render(request, "app/cart.html", {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request):
     if request.method=='GET':
            cart_item_id=request.GET.get('cart_item_id')  
            cart_item=get_object_or_404(Cart,pk= cart_item_id,user=request.user)     
            cart_item.delete()     
     return redirect('cart')                                                                                                                     

def checkout(request):
     if request.method=='POST':
          customer_name=request.POST.get('customer_name')
          mobile_number=request.POST.get('mobile_number')
          address=request.POST.get('address')
          city=request.POST.get('city')
          district=request.POST.get('district')
          pincode=request.POST.get('pincode')
          if not all([customer_name, mobile_number,address,city,district,pincode]):
               messages.error(request,'all requrired')
               return redirect('checkout')
          cart_items=Cart.objects.filter(user=request.user)
          if not cart_items.exists():
               messages.error(request,'your cart empty')
               return redirect('cart')
          order=Order.objects.create(
               user=request.user,
               customer_name=customer_name,
               mobile_number=mobile_number,
               address=address,
               city=city,
               district=district,
               pincode=pincode,
               total_price=sum(item.product.price*item.quantity for item in cart_items),
               payment_method='Cash On Delivery'
               )
          for item in cart_items:
               order.items.create(product=item.product,quantity=item.quantity,price=item.product.price)
               item.delete()
          messages.success(request,'your order has been placed successfully')
          return redirect('home')
     return render(request,'./app/checkout.html')



@login_required
def order_page(request):
     if not request.user.is_authenticated:
        return redirect(f'/?show_login_message=True')
     current_time=timezone.now()
     current_order=Order.objects.filter(user=request.user,created_at__gt=current_time - timedelta(seconds=60))
     previous_order=Order.objects.filter(user=request.user,created_at__lte=current_time - timedelta(seconds=60))
     return render(request,'./app/order_page.html',{'current_order':current_order,'previous_order':previous_order})


@login_required
def rejectorder(request,item_id):
     item=get_object_or_404(OrderItem,id=item_id,order_user=request.user)
     time_difference=timezone.now()-item.created_at
     if time_difference.total_seconds()<=60:
          item.status = 'Rejected'
          item.save()
          messages.success(request,'item rejected succ')
     else:
          messages.error(request,'you can only reject items within 60 seconds of placing the order.')
     return redirect('order_page') 



























# user detaile page code starts
def signup(request):
      if request.method=='POST':
           username=request.POST['username']
           password=request.POST['password']
           confirm=request.POST['confirm']
           if password==confirm:
                
                if User.objects.filter(username=username).exists():
                     
                     return redirect('login')
                else:
                     user=User.objects.create_user(username=username,password=password)
                     login(request,user)

                     return redirect('login')
          
      else:
           return render(request,'./user/signup.html')
def loginview(request):
      if request.method=='POST':
           username=request.POST.get('username')
           password=request.POST.get('password')
           user=authenticate(username=username,password=password)
           if user is not None:
                login(request,user)
                messages.success(request,"you logged in")
                return redirect('login')
           else:
                messages.error(request,'invalid username and password')
                return redirect('login')
      return render(request,'./user/login.html')


def logoutview(request):
     logout(request)
     return render(request,"./app/index.html")
# user detaile page code ends





# Let's say you have a URL like this: http://example.com/?subcatagroy_id=123.

# request.GET would be {'subcatagroy_id': '123'}.
# request.GET.get('subcatagroy_id') would return '123'.
# So, selected_subcategory_id would be '123'.
# Now, you can use selected_subcategory_id to filter your products based on the selected subcategory.