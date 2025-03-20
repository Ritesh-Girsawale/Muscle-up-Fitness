from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product,cart,Address,Order,BMIRecord
from django.db.models import Q
import re 
import random
import razorpay
from django.core.mail import send_mail
from django import forms
from django.contrib import messages 
from django.contrib.auth import views as auth_views

# Create your views here.

def product_details(request,pid):
    context={}
    product=Product.objects.filter(id=pid)
    

    # product=view1.objects.filter(id=pid)
   

    context['product']=product
    return render(request,'product_details.html',context) 





# def filterbycategory(request,cat):
#     context={}
#     products=Product.objects.filter(category=int(cat))

#     context['products']=products
#     return render(request,'body.html',context)        

    



def base(request):
    return render(request,'base.html')

def body(request):
    context={}

    products=Product.objects.all()
    print(products)
    context["products"]=products


    return render(request,'body.html',context)


    # A=Acce.objects.all()
    # context['okay']=A  
    # return render(request,'body.html',context) 


def register(request):
    context={}
    if request.method=='POST':
        un=request.POST['uname']
        em=request.POST['uemail']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        print(un,em,p,cp)
        if un=='' or em=='' or p=='' or cp=='':
            context['error_msg']='ALL FIELDS ARE REQUIRED'
            return render(request,'register.html',context)
       
        elif len(p)<8:
            context['error_msg']='PASSWORD MUST BE  GREATER THAN OR EQUAL TO 8'
            return render(request,'register.html',context)

        elif p!=cp:
            context['error_msg']='PASSWORD AND CONFIRM PASSWORD NOT MATCHED'
            return render(request,'register.html',context)

        else:
            u=User.objects.create(username=un,email=em)
            u.set_password(p)
            u.save()

            return redirect('/login')
        



        
    else:
        return render(request,'register.html')


def ulogin(request):
    context={}
    if request.method=='POST':
        un=request.POST['uname']
        p=request.POST['upass']
        print(un,p)
        if un=='' or p=='':
            context['error_msg']='ALL fileds are required !'
            return render(request,'login.html',context)

        else:
            u=authenticate(username=un,password=p)
            print(u)
            if u !=None:
                login(request,u)
                return redirect('/')

            else:
                context['error_msg']='username and password are not matched!'
                return render(request,'login.html',context)    

    else:
        return render(request,'login.html')


def ulogout(request):
    logout(request)
    return redirect('/')




# def filterbycategory(request,cat):
#     context={}
#     v=Product.objects.filter(category=int(cat))

#     context['key']=v
#     return render(request,'body.html',context)



def filterbycategory(request,cat):
    context={}
    products=Product.objects.filter(category=int(cat))

    context['products']=products
    return render(request,'body.html',context)        


def sortbyprice(request, p):
    context = {}
    if p == '1':
        products = Product.objects.order_by('price').all()  # Ascending
    else:
        products = Product.objects.order_by('-price').all()  # Descending
    context['products'] = products
    return render(request, 'body.html', context)


def filterbyprice(request):
    context = {}

   
    mn = request.GET.get('min', '0')  
    mx = request.GET.get('max', '9999999')  

    
    try:
        mn = int(mn)
        mx = int(mx)
    except ValueError:
        mn, mx = 0, 9999999 


   
    products = Product.objects.filter(Q(price__gte=mn) & Q(price__lte=mx))
    context['products'] = products

    return render(request, 'body.html', context)   

# discount filter

def product_list(request):
    products = Product.objects.filter(is_active=True)

   
    discount_range = request.GET.get('discount_range')

    if discount_range:
        min_discount, max_discount = map(int, discount_range.split('-'))
        
        products = [product for product in products if min_discount <= product.discount_percentage() <= max_discount]

    context = {
        'products': products,
    }
    return render(request, 'body.html', context)
# def filterbydiscount(request):
#     context={}
#     products=Product.objects.filter(discount_percentage)



def addtocart(request,pid):
    context={}
    product=Product.objects.filter(id=pid)
    context['product']=product
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=cart.objects.filter(q1&q2)
        if len(c)==1:

            context['error_msg']='Product already exist in your cart!' 
            return render(request,'product_details.html',context) 
        else:
            c=cart.objects.create(userid=u[0],pid=p[0])
            c.save()
            context['success']='Product added to cart successfully!' 
            return render(request,'product_details.html',context) 
        


    else:
        context['error_msg']="please login first !"
        return render(request,'product_details.html',context)




def viewcart(request):
    carts=cart.objects.filter(userid=request.user.id)
    context={}
    total_amount=0
    items=0
    for i in carts:
        total_amount+=i.pid.price*i.qty
        items+=i.qty
    context['total']=total_amount
    context['items']=items    
    context['carts']=carts
    return render(request,'cart.html',context) 


def shopmore(request):
    return redirect('/')    

def back(request):

    return redirect('/mycart')    



def removecart(request,cid):
    c=cart.objects.filter(id=cid)
    c.delete()
    return redirect('/mycart')          

def updateqty(request,x,cid):
   
    c=cart.objects.filter(id=cid)
    quantity=c[0].qty
    if x=='1':
        quantity+=1
    elif quantity>1:
        quantity-=1   
    c.update(qty=quantity)
    return redirect('/mycart')       


def checkaddress(request):
    context={}
    user=User.objects.filter(id=request.user.id)
    address=Address.objects.filter(user_id=user[0])
    if len(address)>=1:
        return redirect('/placeorder')



    elif request.method=='POST':
        fn=request.POST['full_name']
        ad=request.POST['address']
        ct=request.POST['city']
        st=request.POST['state']
        z=request.POST['zipcode']
        mob=request.POST['mobile']
        if re.match(r"[6-9]\d{9}",mob):
            addr=Address.objects.create(user_id=user[0],fullname=fn,address=ad,city=ct,state=st,pincode=z,mobile=mob)

            addr.save()
            return redirect('/placeorder')


            
        else:
            context['error_msg']='INVALID Mobile number please enter valid number' 
            return render( request,'address.html',context)  
    return render( request,'address.html',context)


# def checkaddress(request):
#     context = {}
#     user = request.user

#     # Fetch all addresses of the logged-in user
#     addresses = Address.objects.filter(user_id=user)
#     context['addresses'] = addresses

#     if request.method == 'POST':
#         fn = request.POST['full_name']
#         ad = request.POST['address']
#         ct = request.POST['city']
#         st = request.POST['state']
#         z = request.POST['zipcode']
#         mob = request.POST['mobile']

#         if not re.match("[6-9]\d{9}", mob):
#             context['error_msg'] = 'INVALID Mobile number, please enter a valid number'
#             return render(request, 'address.html', context)

#         Address.objects.create(
#             user_id=user, fullname=fn, address=ad, city=ct, state=st, pincode=z, mobile=mob
#         )

#         return redirect('/fetchorder')  # Redirect to address selection after adding

#     return render(request, 'address.html', context)



def placeorder(request):
   
    c=cart.objects.filter(userid=request.user.id)
    u=User.objects.filter(id=request.user.id)
    for carts in c:
        orderid=random.randint(1000,10000)
        amount=carts.pid.price*carts.qty
        order=Order.objects.create(order_id=orderid,user_id=u[0],p_id=carts.pid,qty=carts.qty,amt=amount)
        order.save()
        c.delete()

    return redirect('/fetchorder')  

# def placeorder(request):
#     if request.method == 'POST':
#         selected_address_id = request.POST.get('selected_address')
        
#         if not selected_address_id:
#             return redirect('/fetchorder')  # Ensure an address is selected

#         selected_address = Address.objects.get(id=selected_address_id)
#         user = request.user
#         cart_items = cart.objects.filter(userid=user)

#         for cart_item in cart_items:
#             order_id = random.randint(1000, 10000)
#             amount = cart_item.pid.price * cart_item.qty
#             Order.objects.create(
#                 order_id=order_id, 
#                 user_id=user, 
#                 p_id=cart_item.pid, 
#                 qty=cart_item.qty, 
#                 amt=amount
#             )

#         cart_items.delete()  # Clear cart after placing order

#         return redirect('/fetchorder')  # Redirect to fetchorder after placing order

#     return redirect('/fetchorder')  # Ensure form submission is required



def fetchorder(request):

    context={}
    u=User.objects.filter(id=request.user.id)
    address=Address.objects.filter(user_id=u[0])
    q1=Q(user_id=u[0])
    q2=Q(payment_status='unpaid')
    orders=Order.objects.filter(q1&q2)
    context['address']=address
    total=0
    items=0
    for i in orders:
    
        total+=i.amt
        items+=i.qty
    context['total']=total
    context['items']=items  
    return render(request,'fetchorder.html',context)

# def fetchorder(request):
#     context = {}
#     user = request.user
#     orders = Order.objects.filter(user_id=user, payment_status='unpaid')

#     addresses = Address.objects.filter(user_id=user)  # Get all saved addresses
#     context['addresses'] = addresses

#     total = sum(order.amt for order in orders)
#     items = sum(order.qty for order in orders)

#     context['total'] = total
#     context['items'] = items
#     context['orders'] = orders

#     if request.method == 'POST':
#         selected_address_id = request.POST.get('selected_address')
#         if selected_address_id:
#             selected_address = Address.objects.get(id=selected_address_id)
#             context['selected_address'] = selected_address
#             return redirect('/placeorder')  # Proceed to place order with selected address

#     return render(request, 'fetchorder.html', context)


def makepayment(request):
    u=User.objects.filter(id=request.user.id)
    q1=Q(user_id=u[0])
    q2=Q(payment_status='unpaid')
    orders=Order.objects.filter(q1&q2)
    sum=0
    for i in orders:
        sum+=i.amt
        orderid=i.order_id
    context={}
    client=razorpay.Client(auth=("rzp_test_bfwC1cyirb4ypO","6l3qZkBWBwXbene26Wf8ML1L"))
    data={"amount":sum*100,"currency":"INR","receipt":'orderid'}
    payment=client.order.create(data=data)
    context['payment']=payment


    return render(request,'pay.html',context)




from django.core.mail import send_mail
from django.shortcuts import redirect
from .models import Order  # Import the Order model
from datetime import datetime

def email_send(request):
    receiver_email = request.user.email

   
    # product_name = latest_order.p_id.pname
    latest_order = Order.objects.filter(user_id=request.user.id).latest('id')
    current_date = datetime.now().strftime("%d-%m-%Y")

    subject = "🎉 Order Confirmation - Muscle Up"

    message = (
        f"Dear {request.user.first_name if request.user.first_name else 'Customer'},\n\n"
        "Thank you for your order at Muscle Up! 🏋️‍♂️\n\n"
        "We are excited to inform you that your order has been successfully placed.\n"
        "Our team is now processing your order, and you will receive further updates soon.\n\n"
        f"**Order Details:\n"
        f"-order Date:{current_date:}\n"
        # f"-Product Name:#{product_name}\n"
        f"-📅Order Number: #{latest_order.order_id}\n"
        f"-🛒 Estimated Delivery: 3-5 business days\n\n"
        "📦 **Tracking & Updates:**\n"
        "You can track your order status by visiting your account dashboard.\n\n"
        "If you have any questions, feel free to reach out to our support team.\n\n"
        "Thank you for choosing **Muscle Up** – Keep pushing your limits! 💪\n\n"
        "Best Regards,\n"
        "**Muscle Up Team**\n"
        "📩 support@muscleup.com\n"
        "📞 +1 234 567 890"
    )

    send_mail(
        subject,
        message,
        'girsawaleritesh5@gmail.com', 
        [receiver_email],
        fail_silently=False,
    )   

    return redirect('/update_order_status')


def update_order_status(request):
    u=User.objects.filter(id=request.user.id)
    q1=Q(user_id=u[0])
    q2=Q(payment_status='unpaid')
    orders=Order.objects.filter(q1&q2)
    orders.update(payment_status='paid')
    return redirect('/')


def discount_percentage(self):
    if self.price1 > 0:  
        return round(((self.price1 - self.price) / self.price1) * 100, 2)
    return 0 

def my_order(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    context = {}
    user_orders = Order.objects.filter(user_id=request.user.id).order_by('-id')  

    context['orders'] = user_orders
    return render(request, 'my_order.html', context)


class BMIForm(forms.Form):
    height = forms.FloatField(label="Height (in cm)", min_value=10)
    weight = forms.FloatField(label="Weight (in kg)", min_value=1)

def calculate_bmi_category(bmi):
    """Returns BMI category based on the value."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal Weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def bmi_calculator(request):
    bmi = None
    category = None
    bmi_records = BMIRecord.objects.filter(user=request.user) if request.user.is_authenticated else None

    if request.method == "POST":
        form = BMIForm(request.POST)
        if form.is_valid():
            height_cm = form.cleaned_data["height"]  # 
            weight = form.cleaned_data["weight"]
            height_m = height_cm / 100 

            bmi = weight / (height_m ** 2)  # BMI formula
            category = calculate_bmi_category(bmi)

            if request.user.is_authenticated:
                BMIRecord.objects.create(user=request.user, height=height_cm, weight=weight, bmi=bmi, category=category)

    else:
        form = BMIForm()

    return render(request, "bmi_calculator.html", {"form": form, "bmi": bmi, "category": category, "bmi_records": bmi_records})



def build_muscle(request):
    return render(request,'build_muscle.html')

def fat_loss(request):
    return render(request,'fat_loss.html')


def lean_muscle(request):
    return render(request,'lean_muscle.html')

def exercise(request):
    return render(request,'exercise.html')    


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

def contact_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email (configure SMTP settings in settings.py)
        send_mail(
            f"Contact Us - Message from {name}",
            message,
            email,
            ['ritugirsawale4@gmail.com'], 
        )

        # Show success message
        messages.success(request, "We will get back to you soon. Thank you for reaching out! Keep shopping.")

        return redirect('/') 

    return render(request, 'contact.html')
